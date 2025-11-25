# Refactoring Structure Comparison

## Current Structure (Problems)

```
src/
├── components/
│   ├── chains.py          # 122 lines - all chains mixed
│   ├── prompts.py         # 384 lines - all prompts mixed
│   └── tools.py           # 270 lines - all tools mixed
├── config.py              # Settings with required fields
├── edges.py               # Simple conditional edge
├── graph.py               # Graph building + test code mixed
├── nodes.py               # 630 lines - ALL nodes in one file!
├── observability/
│   └── langfuse_setup.py
└── utilities/
    ├── helpers/
    │   ├── LLMProvider.py
    │   ├── logger.py
    │   └── parsers.py
    └── states/
        ├── report_state.py      # Imports from research_state
        ├── research_state.py    # Imports from tool_state
        ├── tool_state.py        # 173 lines of models
        └── shared_state.py       # Just Section model
```

### Problems:
- ❌ `nodes.py` is 630 lines - too large
- ❌ 4 state files with circular dependencies
- ❌ Deep nesting (`utilities/helpers/`, `utilities/states/`)
- ❌ Mixed concerns (chains, prompts, tools all together)
- ❌ Graph building mixed with test code
- ❌ Complex tool orchestration with if/elif chains
- ❌ Too many similar Pydantic models

---

## Proposed Structure (After Refactoring)

```
src/
├── models/                    # All data models
│   ├── __init__.py
│   ├── state.py              # Unified pipeline state
│   ├── tools.py              # Tool query/output models
│   └── report.py             # Report structure models (Header, Section, Footer)
│
├── nodes/                     # Node implementations (split from 630-line file)
│   ├── __init__.py
│   ├── router.py             # router_node (~50 lines)
│   ├── structure.py          # header, section, footer nodes (~150 lines)
│   ├── research.py           # query generation, tool output nodes (~200 lines)
│   ├── writer.py             # detailed writer nodes (~200 lines)
│   └── verification.py       # verify_report_node (~30 lines)
│
├── tools/                     # Tool implementations
│   ├── __init__.py
│   ├── search.py             # DuckDuckGo, Exa, Serper, Tavily
│   ├── github.py             # GitHubInspector
│   ├── arxiv.py              # Arxiv search
│   ├── orchestrator.py       # Tool execution orchestration
│   ├── formatter.py          # Output formatting
│   └── registry.py           # Tool registry for query types
│
├── chains/                    # LangChain chain builders
│   ├── __init__.py
│   └── builders.py           # All chain creation functions
│
├── prompts/                   # Prompt templates
│   ├── __init__.py
│   └── templates.py         # All prompt templates
│
├── graph/                     # Graph building
│   ├── __init__.py
│   ├── builders.py          # Graph builder classes
│   └── factory.py           # Graph factory function
│
├── helpers/                   # Utility functions (flattened)
│   ├── __init__.py
│   ├── llm.py               # LLMProvider (renamed from LLMProvider.py)
│   ├── logger.py            # Logging setup
│   └── parsers.py           # Text parsing utilities
│
├── exceptions.py              # Custom exceptions
├── config.py                  # Configuration (with defaults)
└── __init__.py               # Public API exports
```

---

## Key Improvements

### 1. State Consolidation
**Before**: 4 files with circular dependencies
```
utilities/states/
├── report_state.py      → imports research_state
├── research_state.py    → imports tool_state
├── tool_state.py        → standalone
└── shared_state.py      → standalone
```

**After**: 2-3 focused files
```
models/
├── state.py             # Unified ResearchPipelineState
├── tools.py             # Tool models
└── report.py            # Report structure models
```

### 2. Node Splitting
**Before**: 1 massive file
```
nodes.py (630 lines)
├── router_node
├── header_writer_node
├── section_writer_node
├── footer_writer_node
├── verify_report_node
├── query_generation_node
├── tool_output_node
├── detailed_section_writer_node
├── detailed_header_writer_node
├── detailed_footer_writer_node
└── report_formatter_node
```

**After**: Focused modules
```
nodes/
├── router.py (50 lines)
├── structure.py (150 lines)
├── research.py (200 lines)
├── writer.py (200 lines)
└── verification.py (30 lines)
```

### 3. Tool Orchestration
**Before**: Massive if/elif chain
```python
def get_tool_output(...):
    if type_of_query == "factual_query":
        output.duckduckgo_output = ...
        output.exa_output = ...
    elif type_of_query == "comparative_evaluative_query":
        output.duckduckgo_output = ...
        output.exa_output = ...
        output.serper_output = ...
    # ... 3 more elif blocks
```

**After**: Registry-based
```python
class ToolRegistry:
    QUERY_TYPE_TOOLS = {
        "factual_query": ["duckduckgo", "exa", "tavily"],
        "comparative_evaluative_query": ["duckduckgo", "exa", "tavily", "serper"],
        # ...
    }

def get_tool_output(registry, query_type, queries):
    tools = registry.get_tools_for_type(query_type)
    # Dynamic execution based on registry
```

### 4. Type Simplification
**Before**: 10+ similar classes
```python
class FactualQueryState(BaseModel): ...
class ComparativeQueryState(BaseModel): ...
class ResearchQueryState(BaseModel): ...
class ProgrammingQueryState(BaseModel): ...
class IdeaQueryState(BaseModel): ...
# + 5 more output classes
```

**After**: Unified with optional fields
```python
class ToolQuery(BaseModel):
    query_type: Literal["factual", "comparative", ...]
    duckduckgo_query: Optional[DuckDuckGoQuery] = None
    exa_query: Optional[ExaQuery] = None
    # All tools as optional fields
    # Registry determines which are used
```

### 5. Graph Building
**Before**: Mixed with test code
```python
# graph.py
section_graph = section_builder.compile(...)
research_graph = research_builder.compile(...)
writer_graph = writer_builder.compile(...)

async def main():  # Test code mixed in!
    # ... test execution
```

**After**: Clean separation
```python
# graph/factory.py
def create_all_graphs() -> Tuple[StateGraph, StateGraph, StateGraph]:
    """Create and return all research pipeline graphs."""
    return (
        SectionGraphBuilder().build(),
        ResearchGraphBuilder().build(),
        WriterGraphBuilder().build(),
    )

# tests/test_pipeline.py
async def test_full_pipeline():
    # Test code in proper location
```

---

## Import Path Comparison

### Before (Deep nesting)
```python
from utilities.helpers.LLMProvider import LLMProvider
from utilities.states.report_state import ReportState
from utilities.states.research_state import ResearchState
from components.chains import get_router_chain
```

### After (Flattened)
```python
from src.helpers.llm import LLMProvider
from src.models.state import ResearchPipelineState
from src.chains.builders import get_router_chain
```

---

## File Size Comparison

| File | Before | After | Improvement |
|------|--------|-------|-------------|
| nodes.py | 630 lines | Split into 5 files (~50-200 each) | ✅ Much more manageable |
| research_state.py | 222 lines | Merged into state.py | ✅ Consolidated |
| tool_state.py | 173 lines | Moved to models/tools.py | ✅ Better organized |
| components/chains.py | 122 lines | chains/builders.py | ✅ Same, better location |
| components/prompts.py | 384 lines | prompts/templates.py | ✅ Same, better location |
| components/tools.py | 270 lines | Split into tools/*.py | ✅ Better separation |

---

## Benefits Summary

1. ✅ **Maintainability**: Smaller, focused files
2. ✅ **Testability**: Each module can be tested independently
3. ✅ **Clarity**: Clear separation of concerns
4. ✅ **Extensibility**: Easy to add new nodes, tools, or query types
5. ✅ **No Circular Dependencies**: Clean import structure
6. ✅ **Better Organization**: Logical grouping of related code
7. ✅ **Easier Onboarding**: New developers can understand structure quickly

---

## Migration Checklist

- [ ] Phase 1: Consolidate state management
- [ ] Phase 2: Split nodes into modules
- [ ] Phase 3: Simplify tool orchestration
- [ ] Phase 4: Flatten directory structure
- [ ] Phase 5: Refactor graph building
- [ ] Phase 6: Simplify type system
- [ ] Phase 7: Improve error handling
- [ ] Phase 8: Improve configuration
- [ ] Phase 9: Refactor components
- [ ] Phase 10: Clean up imports
- [ ] Update all tests
- [ ] Update documentation
- [ ] Update app.py imports


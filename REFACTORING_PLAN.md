# Refactoring Plan for Deep Research Codebase

## Executive Summary

The current `src/` folder has several architectural issues that make it difficult to maintain, test, and extend. This plan outlines a systematic refactoring approach to simplify the codebase while maintaining functionality.

## Current Problems Identified

### 1. **State Management Complexity**
- **Issue**: 4 separate state files (`report_state.py`, `research_state.py`, `tool_state.py`, `shared_state.py`) with circular dependencies
- **Impact**: Hard to understand data flow, difficult to modify state structure
- **Evidence**: `report_state.py` imports from `research_state.py`, which imports from `tool_state.py`

### 2. **Monolithic Nodes File**
- **Issue**: `nodes.py` is 630 lines with all node logic mixed together
- **Impact**: Hard to find specific functionality, difficult to test individual nodes
- **Evidence**: Contains router, header, section, footer, query generation, tool output, and writer nodes all in one file

### 3. **Complex Tool Orchestration**
- **Issue**: `get_tool_output()` function has massive if/elif chains (lines 226-318 in nodes.py)
- **Impact**: Adding new query types requires modifying multiple places, error-prone
- **Evidence**: 5 different query types with similar but duplicated logic

### 4. **Type Explosion**
- **Issue**: Too many similar Pydantic models (FactualQueryState, ComparativeQueryState, ResearchQueryState, etc.)
- **Impact**: Code duplication, maintenance burden
- **Evidence**: `research_state.py` has 10+ similar model classes

### 5. **Graph Building Complexity**
- **Issue**: `graph.py` mixes graph building with test code
- **Impact**: Confusing structure, test code in production module
- **Evidence**: Lines 76-132 contain `main()` function with test code

### 6. **Inconsistent Import Patterns**
- **Issue**: Mix of relative and absolute imports, circular dependencies
- **Impact**: Import errors, unclear module relationships
- **Evidence**: Some files use `from utilities.states...`, others use `from components...`

### 7. **Deep Nesting**
- **Issue**: Unnecessary folder nesting (`utilities/helpers/`, `utilities/states/`)
- **Impact**: Long import paths, harder navigation
- **Evidence**: `from utilities.helpers.LLMProvider import LLMProvider`

### 8. **Mixed Concerns**
- **Issue**: Components folder mixes chains, prompts, and tools
- **Impact**: Unclear boundaries, tight coupling
- **Evidence**: `components/chains.py` imports from `components/prompts.py` and `utilities/`

### 9. **Error Handling Inconsistency**
- **Issue**: Some functions return None on error, others return empty objects, some use try/except
- **Impact**: Unpredictable behavior, hard to debug
- **Evidence**: Inconsistent patterns across nodes.py

### 10. **Config Management**
- **Issue**: Settings class requires all keys, hard to test without full config
- **Impact**: Difficult to test, tightly coupled to environment
- **Evidence**: `config.py` has no defaults for required fields

---

## Refactoring Strategy

### Phase 1: Consolidate State Management

**Goal**: Reduce state files from 4 to 1-2, eliminate circular dependencies

**Actions**:
1. **Create unified state file** (`src/models/state.py`)
   - Merge `ReportState`, `ResearchState`, `WriterState` into a single `ResearchPipelineState`
   - Use optional fields to represent different stages
   - Move shared models (`Section`, `Header`, `Footer`) to `src/models/`

2. **Consolidate tool models** (`src/models/tools.py`)
   - Move all tool-related Pydantic models from `tool_state.py` here
   - Create a unified `ToolQuery` and `ToolOutput` with discriminated unions
   - Replace 5 query state classes with a single class using optional fields

3. **Delete old state files**:
   - Remove `utilities/states/report_state.py`
   - Remove `utilities/states/research_state.py`
   - Remove `utilities/states/tool_state.py`
   - Remove `utilities/states/shared_state.py`

**Benefits**:
- Single source of truth for state
- No circular dependencies
- Easier to understand data flow

---

### Phase 2: Split Nodes into Modules

**Goal**: Break down 630-line `nodes.py` into focused, testable modules

**Actions**:
1. **Create node modules**:
   ```
   src/nodes/
   ├── __init__.py
   ├── router.py          # router_node
   ├── structure.py        # header_writer_node, section_writer_node, footer_writer_node
   ├── research.py         # query_generation_node, tool_output_node
   ├── writer.py           # detailed_*_writer_node, report_formatter_node
   └── verification.py    # verify_report_node
   ```

2. **Extract helper functions**:
   - Move `get_tool_output()` to `src/tools/orchestrator.py`
   - Move `roll_out_output()` to `src/tools/formatter.py`

3. **Update imports** in `graph.py` to use new structure

**Benefits**:
- Each file < 200 lines
- Easy to find specific functionality
- Better testability

---

### Phase 3: Simplify Tool Orchestration

**Goal**: Replace if/elif chains with strategy pattern or registry

**Actions**:
1. **Create tool registry** (`src/tools/registry.py`):
   ```python
   class ToolRegistry:
       def __init__(self):
           self.tools = {}
           self.query_types = {}
       
       def register(self, query_type: str, tools: List[str]):
           self.query_types[query_type] = tools
   ```

2. **Refactor `get_tool_output()`**:
   - Use registry to determine which tools to call
   - Use dynamic attribute setting instead of if/elif
   - Create `ToolExecutor` class to handle execution

3. **Create tool factory** (`src/tools/factory.py`):
   - Factory pattern to create appropriate tool instances
   - Reduces duplication

**Benefits**:
- Adding new query types = adding to registry
- No more massive if/elif chains
- Easier to test individual tools

---

### Phase 4: Flatten Directory Structure

**Goal**: Reduce nesting depth, make imports simpler

**Actions**:
1. **Move files up one level**:
   ```
   Current:                    New:
   utilities/helpers/         helpers/
   utilities/states/          models/
   components/                components/ (keep as is)
   ```

2. **Reorganize**:
   ```
   src/
   ├── models/           # All Pydantic models
   │   ├── state.py
   │   ├── tools.py
   │   └── report.py
   ├── nodes/            # Node implementations
   │   ├── router.py
   │   ├── structure.py
   │   └── ...
   ├── tools/            # Tool implementations
   │   ├── search.py
   │   ├── github.py
   │   ├── orchestrator.py
   │   └── registry.py
   ├── chains/           # LangChain chains
   │   └── builders.py
   ├── prompts/          # Prompt templates
   │   └── templates.py
   ├── helpers/          # Utility functions
   │   ├── llm.py
   │   ├── logger.py
   │   └── parsers.py
   ├── graph.py          # Graph building only
   └── config.py         # Configuration
   ```

**Benefits**:
- Shorter import paths
- Clearer organization
- Easier navigation

---

### Phase 5: Refactor Graph Building

**Goal**: Separate graph building from test code, make it more declarative

**Actions**:
1. **Create graph builders** (`src/graph/builders.py`):
   ```python
   class SectionGraphBuilder:
       def build(self) -> StateGraph:
           # Clean graph building logic
   ```

2. **Move test code** to `tests/` or `examples/`

3. **Create graph factory** (`src/graph/factory.py`):
   - Single function to create all graphs
   - Handles checkpointer setup
   - Returns compiled graphs

**Benefits**:
- Production code separated from test code
- Easier to understand graph structure
- Better testability

---

### Phase 6: Simplify Type System

**Goal**: Reduce number of similar Pydantic models

**Actions**:
1. **Use discriminated unions**:
   ```python
   class ToolQuery(BaseModel):
       query_type: Literal["factual", "comparative", ...]
       # All optional fields for different tools
       duckduckgo_query: Optional[DuckDuckGoQuery] = None
       exa_query: Optional[ExaQuery] = None
       # ... etc
   ```

2. **Create base classes**:
   - `BaseToolQuery` with common fields
   - `BaseToolOutput` with common fields
   - Use composition instead of inheritance where possible

3. **Use TypedDict for simple structures**:
   - Replace simple Pydantic models with TypedDict where validation isn't needed

**Benefits**:
- Less code duplication
- Easier to extend
- Better type safety

---

### Phase 7: Improve Error Handling

**Goal**: Consistent error handling patterns

**Actions**:
1. **Create custom exceptions** (`src/exceptions.py`):
   ```python
   class NodeExecutionError(Exception): pass
   class ToolExecutionError(Exception): pass
   class StateValidationError(Exception): pass
   ```

2. **Standardize return patterns**:
   - All nodes return dict updates (current pattern is good)
   - Use Result/Either pattern for operations that can fail
   - Log errors consistently

3. **Add error recovery**:
   - Default values for failed operations
   - Graceful degradation

**Benefits**:
- Predictable error handling
- Easier debugging
- Better user experience

---

### Phase 8: Improve Configuration

**Goal**: Make config more testable and flexible

**Actions**:
1. **Add defaults** to Settings:
   ```python
   class Settings(BaseSettings):
       TOGETHER_API_KEY: str = ""
       EXA_API_KEY: str = ""
       # ... with sensible defaults
   ```

2. **Create config validator**:
   - Check required keys at runtime
   - Provide helpful error messages

3. **Support config files**:
   - Allow `.env` file
   - Support different configs for dev/test/prod

**Benefits**:
- Easier testing
- Better error messages
- More flexible deployment

---

### Phase 9: Refactor Components

**Goal**: Better separation of concerns in components

**Actions**:
1. **Split chains.py**:
   - One file per chain type
   - Or use a builder pattern

2. **Extract prompt management**:
   - Move prompts to separate files
   - Use template system

3. **Organize tools**:
   - Group related tools together
   - Create tool interfaces

**Benefits**:
- Clearer boundaries
- Easier to modify
- Better testability

---

### Phase 10: Clean Up Imports

**Goal**: Consistent import patterns, no circular dependencies

**Actions**:
1. **Standardize on absolute imports**:
   - Use `from src.models import ...` consistently
   - Or use relative imports consistently

2. **Create `__init__.py` files**:
   - Export public API
   - Hide internal details

3. **Fix circular dependencies**:
   - Use TYPE_CHECKING for type hints
   - Move shared code to common module

**Benefits**:
- No import errors
- Clear module boundaries
- Easier refactoring

---

## Implementation Order

1. **Phase 1** (State consolidation) - Foundation for everything else
2. **Phase 4** (Flatten structure) - Makes other phases easier
3. **Phase 2** (Split nodes) - Improves maintainability
4. **Phase 3** (Tool orchestration) - Reduces complexity
5. **Phase 6** (Type system) - Simplifies code
6. **Phase 5** (Graph building) - Clean up structure
7. **Phase 7** (Error handling) - Improve robustness
8. **Phase 8** (Configuration) - Improve testability
9. **Phase 9** (Components) - Final cleanup
10. **Phase 10** (Imports) - Polish

---

## Migration Strategy

### For Each Phase:

1. **Create new structure** alongside old code
2. **Update imports gradually** - start with one module
3. **Test thoroughly** after each change
4. **Delete old code** only after new code is proven
5. **Update documentation** as you go

### Testing Strategy:

1. **Unit tests** for each node
2. **Integration tests** for graph execution
3. **End-to-end tests** for full pipeline
4. **Regression tests** to ensure no functionality lost

---

## Success Metrics

- **Lines of code**: Reduce by ~30%
- **File count**: Reduce from ~15 to ~25 (more, smaller files)
- **Max file size**: No file > 300 lines
- **Import depth**: Max 2 levels deep
- **Cyclomatic complexity**: Reduce average by 40%
- **Test coverage**: Maintain or improve

---

## Risks and Mitigation

### Risk 1: Breaking existing functionality
- **Mitigation**: Comprehensive test suite before refactoring
- **Mitigation**: Gradual migration, keep old code until new works

### Risk 2: Team confusion during refactoring
- **Mitigation**: Clear documentation of new structure
- **Mitigation**: Communication plan for changes

### Risk 3: Time investment
- **Mitigation**: Phased approach allows stopping at any point
- **Mitigation**: Each phase delivers value independently

---

## Estimated Effort

- **Phase 1**: 4-6 hours
- **Phase 2**: 6-8 hours
- **Phase 3**: 4-6 hours
- **Phase 4**: 2-3 hours
- **Phase 5**: 2-3 hours
- **Phase 6**: 3-4 hours
- **Phase 7**: 2-3 hours
- **Phase 8**: 2-3 hours
- **Phase 9**: 3-4 hours
- **Phase 10**: 2-3 hours

**Total**: ~30-45 hours

---

## Notes

- This is a **plan only** - implementation should be done incrementally
- Each phase can be done independently
- Some phases can be done in parallel (e.g., Phase 2 and Phase 3)
- Consider using automated refactoring tools where possible
- Keep git history clean with meaningful commits per phase


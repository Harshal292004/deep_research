from utilities.app_state import RouterResponse,AppState
from utilities.LLMProvider import LLMProvider
from chains import  get_router_chain,get_header_chain,get_section_writer_chain,get_footer_writer_chain,get_refrences_writter_chain,get_verify_report_framework_chain
from utilities.report_state import Section,Sections,Footer,Header,Reference,ReportState

def router_node(state:ReportState):
    query=state.query
    chain= get_router_chain()
    response=chain.invoke(
        {
            "query":query
        }
    )
    type_of_query =response.type_of_query
    return{
        "type_of_query":type_of_query
    }


def header_writer_node(state:ReportState):
    query= state.query
    type_of_query= state.type_of_query
    chain= get_header_chain()
    response=chain.invoke(
        {
            "query":query,
            "type_of_query":type_of_query
        }
    )
    return {
        "header":{
            "title":response.title,
            "summary":response.summary,
        }
    }

def section_writer_node(state:ReportState):
    query= state.query
    type_of_query= state.type_of_query
    title_of_report=state.header.title
    summary_of_report= state.header.summary
    chain= get_section_writer_chain()
    response= chain.invoke(
        {
            "query":query,
            "type_of_query":type_of_query,
            "title":title_of_report,
            "summary":summary_of_report
        }
    )
    sections=response.sections
    ouptut=[]
    for sec in sections:
        ouptut.append(
            {
                "section_id":sec.section_id,
                "name":sec.name,
                "description":sec.description ,
                "research":sec.research,
                "content":sec.content
            }
        )
    
    return{
        "sections":output
    }

def footer_writer_node(state:ReportState):
    query= state.query
    type_of_query= state.type_of_query
    sections= state.sections
    chain= get_footer_writer_chain()
    section_string=""
    
    for sec in sections:
        section_string.join(f"\n section_id:{sec.section_id} name: {sec.name} description: {sec.description} research: {sec.research} content: {sec.content}")
    
    response=chain.invoke(
        {
            "query":query,
            "type_of_query":type_of_query,
            "sections":section_string
        }
    )
    
    return {
        "footer": {
            "conclusion":response.conclusion
        }
    }


def refrence_writer_node(state:ReportState):
    query= state.query
    type_of_query= state.type_of_query
    chain= get_refrences_writter_chain()
    sections=state.sections
    for sec in sections:
        section_string.join(f"\n section_id:{sec.section_id} name: {sec.name} description: {sec.description} research: {sec.research} content: {sec.content}")
    
    response=chain.invoke(
        {
            "query":query,
            "type_of_query":type_of_query,
            "sections":section_string
        }
    )
    output_ref=[]
    for ref in response.refreces:
        output_ref.append(
            {
                "section_id":ref.section_id,
                "section_name":ref.section_name,
                "source_url": ref.source_url
            }
        )
    
    return {
        "refrences":{
            "refrences":output_ref
        }
    }
    

def verify_report_framework_node(state:ReportState):
    chain= get_verify_report_framework_chain()
    report_string=""
    
    report_string.join(f"\n ##Header \n {state.header.title} {state.header.summary} \n\n ## Sections \n")
    for sec in state.sections:
        report_string.join(f"\n section_id:{sec.section_id} name: {sec.name} description: {sec.description} research: {sec.research} content: {sec.content} \n\n")
    
    report_string.join(f"## Footer \n {state.footer.conclusion} \n\n")
    
    response= chain.invoke(
        {
            "report_structure":report_string
        }
    )
    
    return{
        "report_framework_good":response.verified
    }
    
from components.prompts import Prompts


output= Prompts.get_router_prompt().invoke({"query":"Whats the poin of the world"})
print(output)
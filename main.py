import os
import importlib
from server import mcp

tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
for filename in os.listdir(tools_dir):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]
        importlib.import_module(f'tools.{module_name}')

if __name__ == "__main__":
    mcp.run()
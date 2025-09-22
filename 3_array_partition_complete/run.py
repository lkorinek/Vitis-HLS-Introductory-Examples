
import vitis
import os

cwd = os.getcwd()+'/'

# Initialize session
client = vitis.create_client()
client.set_workspace(path='./w')

component_name = 'array_partition_complete_read_A_B_opt'

# Delete the component if it already exists
if os.path.exists(f'./w/{component_name}'):
	client.delete_component(name=component_name)

# Create component. Create new config file in the component folder of the workspace
comp = client.create_hls_component(name=component_name, cfg_file = ['hls_config.cfg'], template = 'empty_hls_component')

# Get handle of config file, then programmatically set desired options
cfg_file = client.get_config_file(path = f'./w/{component_name}/hls_config.cfg')
cfg_file.set_value (                 key = 'part',                  value = 'xcvu9p-flga2104-2-i') 
cfg_file.set_value (section = 'hls', key = 'syn.file',              value = cwd+'matmul_partition.cpp')
cfg_file.set_values(section = 'hls', key = 'tb.file',               values = [cwd+'matmul_partition_test.cpp'])
cfg_file.set_value (section = 'hls', key = 'syn.top',               value = 'matmul_partition')
cfg_file.set_value (section = 'hls', key = 'clock',                 value = '4') # 250MHz
cfg_file.set_value (section = 'hls', key = 'flow_target',           value = 'vitis')
cfg_file.set_value (section = 'hls', key = 'package.output.syn',    value = '0')
cfg_file.set_value (section = 'hls', key = 'package.output.format', value = 'xo')
cfg_file.set_value (section = 'hls', key = 'csim.code_analyzer',    value = '0')

# Run flow steps
comp = client.get_component(name=component_name)
comp.run(operation='C_SIMULATION')
comp.run(operation='SYNTHESIS')
comp.run(operation='CO_SIMULATION')

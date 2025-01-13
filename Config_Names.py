from dataclasses import dataclass

@dataclass
class config_naming:
	instance_id : str = "instance_name"
	local_config_path : str = "local_config_path"
	local_git_repro : str = "local_git_repro_path"
	blacklist : str = "file_blacklist"
	whitelist : str = "file_whitelist"
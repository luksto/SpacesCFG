from dataclasses import dataclass

@dataclass
class config_naming:
	prefix : str = "instance_prefix"
	dst_path : str = "destination_path"
	scr_path : str = "source_path"
	blacklist : str = "blacklist_files"
	whitelist : str = "whitelist_files"
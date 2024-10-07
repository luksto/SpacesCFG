import configparser
from pathlib import Path

# Configuration Key-Value default pairs
##      [labor-orca] # Labor Space Orca profile Section
##      instance_name       = "LAB"
##      local_config_path   = "/home/luke/.config/OrcaSlicer/"
##      git_local_repro     = "/home/luke/git/Labor3D_Orca/"
##      file_blacklist      = []
##      file_whitelist       = []

class config_naming:
    instance_id = "instance_name"
    local_config_path = "local_config_path"
    local_git_prepro = "git_local_repro"
    blacklist = "file_blacklist"
    whitelist = "file_whitelist"

def sync_section(para_section) -> bool:
    # read & check all pathes is the section
    # check for no deadlocks in whithe-blacklists
    
    pass


def main(para_cfg_path:str = None) -> bool:
    default_str_cfg_path = "config.cfg"

    # Check and get config file Path
    cfg_path = 0
    if para_cfg_path is None or para_cfg_path == "":
        cfg_path = Path(default_str_cfg_path)
        if not cfg_path.is_file():
            print(f"ERR: no Path for Config-file is given, and the default path {default_str_cfg_path} is no file")
            return False
    else:
        cfg_path = Path(para_cfg_path)
        if not cfg_path.is_file():
            print(f"ERR: given Cinfig file path -{para_cfg_path}- is not available or no file")
            return False
    print(f"LOG: Use cfgfile: {cfg_path.absolute()}")

    config = configparser.ConfigParser()
    config.read(cfg_path)

    # Check for space sections
    if len(config.sections()) < 1:
        print("ERR: no Space-section is found, check your config")
        return False
    
    # go throu each space section and perferm a sychronisation
    spaces = config.sections()
    print(f"vLOG: use spaces: {spaces}")
    for space in spaces:
        sect = config[space]
        print(sect["git_local_repro"])
        # todo: execute function for syncronisation on the particular section. all datas are stored in the section variables.

    # Done


if __name__ == "__main__":
    main()

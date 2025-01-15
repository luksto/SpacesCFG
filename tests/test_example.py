import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from scr.Section_Sync import Section_Sync
from configparser import ConfigParser
from loguru import logger

class TestSection_Sync:
	def test_debug(self):
		config = ConfigParser()
		cfg_path = Path("./tests/config_test.cfg").absolute()
		assert cfg_path.is_file()
		config.read(cfg_path)
		assert config is not None
		assert len(config.sections()) > 0
		section_str = config.sections()[0]
		section = config[section_str]
		for i in section:
			logger.debug(f"{i} = {section[i]}")
		tst_sync = Section_Sync(section) # use first section
		logger.debug(f"Got section obj: {tst_sync}")
		logger.debug(f"name: {tst_sync.name}")
		logger.debug(f"prefix: {tst_sync.prefix} type: {type(tst_sync.prefix)}")
		logger.debug(f"ret type is: {type(tst_sync)}")
		assert tst_sync is not None
		logger.debug(f"ret name is: {tst_sync.name}")
		assert tst_sync.prefix == "LAB"

	def test_debug2(self):
		config = ConfigParser()
		cfg_path = Path("./tests/config_test.cfg").absolute()
		config.read(cfg_path)
		section_str = config.sections()[0]
		section = config[section_str]
		
		# Debug section content before creating Section_Sync
		logger.debug(f"Section type: {type(section)}")
		logger.debug(f"Section content: {dict(section)}")
		logger.debug(f"Prefix value: {section.get('instance_prefix')} of type: {type(section.get('instance_prefix'))}")
		
		# Create with type checking
		tst_sync = Section_Sync(section)
		logger.debug(f"tst_sync.prefix type: {type(tst_sync.prefix)}")
		logger.debug(f"tst_sync.prefix value: {tst_sync.prefix}")
		
		# Assert with string comparison
		assert isinstance(tst_sync.prefix, str), "Prefix should be string"
		assert tst_sync.prefix == "LAB"

if __name__ == "__main__":
	test = TestSection_Sync()
	test.test_debug()
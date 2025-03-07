import configparser
config = configparser.ConfigParser()

config.read("config.ini")
final_cnfg = {}
for section_name in config.sections():
    final_cnfg[section_name] = dict(config[section_name])
# print(final_cnfg)


if __name__ == "__main__":
    print(final_cnfg)
import utils.consts as consts
import json

def load_json(prFilePath):
    with open(prFilePath, "r") as file:
        data = json.load(file)

    return data

def get_profiles():
    return load_json(consts.PROFILE_CONFIG)["profiles"]

def get_profile_by_index(prProfileIndex):
    return get_profiles()[prProfileIndex]
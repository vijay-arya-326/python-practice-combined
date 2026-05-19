import os


def verify_environment_variables_for_business_discovery_agent():
    mandatory_list = [
        "APP_NAME",
        "GEMMA_MODEL",
        "MISTRAL_MODEL",
        "LLAMA_MODEL",
        "GEMMA4_MODEL",
    ]

    optional_list = [
        "OPTIONAL_VAL"
    ]

    mandatory_error_list = []
    optional_error_list = []

    error_flag = False
    start_application = True

    for mandatory in mandatory_list:
        if not os.getenv(mandatory, None):
            start_application = False
            error_flag = True
            mandatory_error_list.append(f"{mandatory} flag missing from environment - mandatory")

    for optional in optional_list:
        if not os.getenv(optional, None):
            error_flag = True
            optional_error_list.append(f"{optional} flag missing from environment - optional")

    return {
        "start_application": start_application,
        "error_flag": error_flag,
        "mandatory_error_list": mandatory_error_list,
        "optional_error_list": optional_error_list
    }

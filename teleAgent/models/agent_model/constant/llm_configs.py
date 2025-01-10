import autogen
dpsk_config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        file_location="teleAgent/services",
        filter_dict={
            "model": [ "deepseek-chat"],#"deepseek-chat", "qwen-plus" "gpt-3.5-turbo-0125", "gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
        },
    )

dalle_config = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "dall-e-3"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.7, 
              }


llm_config_dpsk = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "deepseek-chat"],#"deepseek-chat", "qwen-plus" "gpt-3.5-turbo-0125", "gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_gpt4o = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "gpt-4o"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_gpt4o_unstructured = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "gpt-4o"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
              }


llm_config_gpt4turbo = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "gpt-4-turbo"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_gpt4omini = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "gpt-4o-mini"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_qwenlong = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "qwen-long"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }
llm_config_qwenmax = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "qwen-long"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_claud35snt = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "claude-3-5-sonnet-20240620"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }

llm_config_claud3hk = {"config_list": autogen.config_list_from_json(
                                        "OAI_CONFIG_LIST",
                                        file_location="teleAgent/services",
                                        filter_dict={
                                            "model": [ "claude-3-haiku-20240307"],
                                        },
                                 ),
                    "seed": 42,
                    "cache_seed": 42 , 
                    "temperature": 0.3, 
                    "response_format": { "type": "json_object" } 
              }
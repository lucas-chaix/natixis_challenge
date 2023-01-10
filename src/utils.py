import pandas as pd

def find_closest(ram, ram_refs):
    '''
    Find the closest value to a float in a list of floats.

    Args:
        ram : float = value to find the closest of
        ram_refs : list(float) = reference values
    Return: 
        ram_final : float = closets reference value.
    '''
    for index, ram_ref in enumerate(ram_refs):
        # Initialization
        if index==0:
            ram_final = ram_refs[0]

        # Reccurence
        else:
            if abs(ram-ram_ref) < abs(ram-ram_final):
                ram_final = ram_ref

    return ram_final


def calculate_price(df_cockpit, df_mycloud):
    '''
    Calculate the price of a configuration.

    Args:
        df_cockpit : pandas.DataFrame = table of the configuration
        df_mycloud : pandas.DataFrame = table of the catalogue of prices of mycloud servors
    Return:
        price : float = total price of the configuration
    '''
    # Extract usable data : mycloud servors only
    config = pd.DataFrame(df_cockpit[df_cockpit.mycloud=='Yes'][["iua", "ram", "number_cpu", "name_server"]].sort_values("ram"))
    # Convert in GBytes
    config["ram"] = config.ram/1000 

    # Extract the list of servers (multiple applications correspond to one server)
    info_servers = config[["ram", "number_cpu", "name_server"]].drop_duplicates()
    
    # Find the servors in the catalogue
    info_servers["ram_ref"] = info_servers.ram.apply(lambda x: find_closest(x, df_mycloud.RAM))

    # Add prices
    info_servers = info_servers.merge(df_mycloud, how="left", left_on=["ram_ref", "number_cpu"], right_on=["RAM", "CPU"])
    info_servers = info_servers.drop(["number_cpu", "ram_ref"], axis=1)

    # Calculate the price.
    config_price = info_servers.Price.sum()

    return config_price
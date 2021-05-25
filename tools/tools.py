import pandas as pd


def default_evaluation_parameters():
    """
    Returns default dictionary for evaluation parameters. These are further
    described in the methodology section of the paper. When used for own
    purposes, it can be adapted or own methods can be implemented.

    The evaluation follows dependant on the type of the dictionary entry.

    * list: All list entries are weighted equally. The sum of existing list
    entries in the model is divided by the total number of list entries.
    * dict: The keys of the dictionaries are iterated and checked for their
    existence in the model parameters. The rate/entry of the first existing key
    is chosen as the score. Therefore make sure to choose the highest ranked
    answer as first entry and have the dictionary entries in the right order.
    * string: An own function for the evaluation of this parameter is used.
    This has to be added to 'get_weighted_models_from_evaluation_dicts' method.

    :return: dict
    """
    evaluation_parameters = {
        # General
        'geographic scope': ['local (NUTS3)/used', 'local (NUTS3)/pos',
                             'regional (NUTS1-2)/pos',
                             'regional (NUTS1-2)/used',
                             'national/pos', 'national/used',
                             'international/pos',
                             'international/used'],
        'temporal scope': ['very short/pos', 'very short/used', 'short/pos',
                           'short/used', 'intermediate/pos',
                           'intermediate/used',
                           'long/pos', 'long/used'],
        'temporal resolution': ['<hourly/used', '<hourly/pos',
                                'hourly/pos', 'hourly/used',
                                'intermediate/pos',
                                'intermediate/used', 'annual/pos',
                                'annual/used'],
        'Decision making': 'decision making',
        'efficiency': {'efficiency function': 1.0,
                       'efficiency fixed value': 0.5},
        'ramping': {'ramping yes': 1.0},
        'response time': {'response time yes': 1.0},
        'recovery time': {'recovery time yes': 1.0},
        'probability': {'prob yes': 1.0},
        # Network
        'Distribution Grid': {'Distribution Grid/def': 1.0,
                              'Distribution Grid/pos': 0.5},
        'Transmission Grid': {'Transmission Grid/def': 1.0,
                              'Transmission Grid/pos': 0.5},
        'Smart Grid': {'Smart Grid/def': 1.0, 'Smart Grid/pos': 0.5},
        'Microgrid': {'Microgrid/def': 1.0, 'Microgrid/pos': 0.5},
        'network extension': {'network extension/def': 1.0,
                              'network extension/pos': 0.5},
        'switches': {'switches/def': 1.0, 'switches/pos': 0.5},
        'interconnectors': {'interconnectors/def': 1.0,
                            'interconnectors/pos': 0.5},
        'Grid representation': 'grid representation',
        'grid ancillary services': ['spinning reserve', 'balancing energy',
                                    'sheddable loads',
                                    'Feed-in management', 'redispatch',
                                    'power factor correction',
                                    'curtailment', 'black start'],
        'import': {'flow based': 1.0, 'simplified': 0.5},
        # Supply
        'coal': {'hard coal/def': 1.0, 'hard coal/pos': 0.5},
        'lignite': {'lignite/def': 1.0, 'lignite/pos': 0.5},
        'oil': {'oil/def': 1.0, 'oil/pos': 0.5},
        'natural gas': {'natural gas/def': 1.0, 'natural gas/pos': 0.5},
        'CCGT': {'CCGT/def': 1.0, 'CCGT/pos': 0.5},
        'OCGT': {'OCGT/def': 1.0, 'OCGT/pos': 0.5},
        'CHP': {'CHP/def': 1.0, 'CHP/pos': 0.5},
        'bioenergy': {'Bioenergy/def': 1.0, 'Bioenergy/pos': 0.5},
        'Hydro reservoir': {'hydropower reservoir/def': 1.0,
                            'hydropower reservoir/pos': 0.5},
        'geothermal energy': {'geothermal/def': 1.0, 'geothermal/pos': 0.5},
        'concentrated solar': {'concentrated solar power/def': 1.0,
                               'concentrated solar power/pos': 0.5},
        'photovoltaic': {'photovoltaic/def': 1.0, 'photovoltaic/pos': 0.5},
        'wind onshore': {'wind onshore/def': 1.0, 'wind onshore/pos': 0.5},
        'wind offshore': {'Wind-offshore/def': 1.0, 'Wind-offshore/pos': 0.5},
        'river hydro': {'Run-of-river hydro/def': 1.0,
                        'Run-of-river hydro/pos': 0.5},
        'wave power': {'wave power/def': 1.0, 'wave power/pos': 0.5},
        'tidal power': {'tidal power/def': 1.0, 'tidal power/pos': 0.5},
        'PEM-FC': {'PEM-FC/def': 1.0, 'PEM-FC/pos': 0.5},
        'SOFC': {'SOFC/def': 1.0, 'SOFC/pos': 0.5},
        'curtailed operation': {'curtailed operation yes': 1.0},
        'nuclear': {'Nuclear/def': 1.0, 'Nuclear/pos': 0.5},
        'minimum load': {'minimum load yes': 1.0},
        'discrete capacity expansion': {'discrete expansion yes': 1.0},
        # Demand
        'social factors': {'social yes': 1.0},
        'households': {'households/def': 1.0, 'households/pos': 0.5},
        'industrial load': {'industrial load/def': 1.0,
                            'industrial load/pos': 0.5},
        'service sector': {'service sector/def': 1.0,
                           'service sector/pos': 0.5},
        'maximum deferrable load':
            {'time- and type-dependent': 1.0, 'Type-dependent': 2 / 3,
             'Time-dependent': 2 / 3, 'max def load fixed value': 1 / 3},
        'shifting time': {'shifting time yes': 1.0},
        'price elasticity': {'price elasticity yes': 1.0},
        # Storage
        'Batteries': {'Batteries/def': 1.0, 'Batteries/pos': 0.5},
        'storage implementation': {'dynamic': 1.0, 'fixed/static': 0.5},
        'aging': ['cycle aging', 'calendrical aging'],
        'self discharge': {'self discharge yes': 1.0},
        'PHS': {'PHS/def': 1.0, 'PHS/pos': 0.5},
        'CAES': {'CAES/def': 1.0, 'CAES/pos': 0.5},
        'Caps': {'Caps/def': 1.0, 'Caps/pos': 0.5},
        'Flywheels': {'Flywheels/def': 1.0, 'Flywheels/pos': 0.5},
        # Sector Coupling
        'P2G': {'P2Gas/def': 1.0, 'P2Gas/pos': 0.5},
        'P2H2': {'P2H2/def': 1.0, 'P2H2/pos': 0.5},
        'HP': {'HP/def': 1.0, 'HP/pos': 0.5},
        'EV': {'EV/def': 1.0, 'EV/pos': 0.5},
        'Fuels': {'Fuels (H2)/def': 1.0, 'Fuels (H2)/pos': 0.5},
        'Heat storage': {'Heat storage/def': 1.0, 'Heat storage/pos': 0.5},
        'V2G': {'V2Grid/def': 1.0, 'V2Grid/pos': 0.5},
        'Heat': 'heat',
        'Transport': 'transport',
        'sector coupling supply': 'sector coupling supply',
        'sector coupling demand': 'sector coupling demand',
        'sector coupling storage': 'sector coupling storage'
    }
    return evaluation_parameters


def get_weighted_models_from_evaluation_dicts(models, parameters_with_weights,
                                              evaluation_parameters, table):
    """
    Method to get rated fulfillment of predefined criteria with weighting.

    :param models: List of str with names of models to be evaluated
    :param parameters_with_weights: dict with weighting in the form
        {field_1: {parameter_name_1_1: weighting_1, parameter_1_2: weighting_2, ...},
        field_2: ...}
    :param evaluation_parameters: dict with fulfillment criteria in the form
        {parameter_name_1_1: {  criteria_1: rated_fulfillment,
                                criteria_2: rated_fulfillment, ...},
        parameter_name_1_2: {...}, ...}
    :param table: pandas.DataFrame with survey information, models have to be
        indices of this table and criteria_i have to be column names of this
        dataframe.
    :return: pandas.DataFrame
        Index are entries of inserted list models
        Columns are the keys of inserted dict parameters_with_weights
    """
    weighted_models = {}
    for model in models:
        weighted_models[model] = {}
        for field, parameter_with_weight in parameters_with_weights.items():
            sum_weighting = 0
            sum_model = 0
            for parameter, weight in parameter_with_weight.items():
                sum_weighting += weight
                if isinstance(evaluation_parameters[parameter], dict):
                    for key, evaluation in evaluation_parameters[parameter].\
                            items():
                        if table.loc[model, key] == 1:
                            sum_model += evaluation * weight
                            break
                # special case for uniform representation
                # (e.g. grid ancillary services)
                elif isinstance(evaluation_parameters[parameter], list):
                    sum_parameter = 0
                    for key in evaluation_parameters[parameter]:
                        if table.loc[model, key] == 1:
                            sum_parameter += 1
                    sum_model += \
                        sum_parameter / len(
                            evaluation_parameters[parameter]) * weight
                # special case for more complex functions (e.g. sector
                # representation), if more functions are specified,
                # if-statements have to be added similar like in
                # get_rated_operation_repr_by_name()
                elif isinstance(evaluation_parameters[parameter], str):
                    if evaluation_parameters[parameter] == 'heat' or \
                            evaluation_parameters[parameter] == 'transport':
                        sum_model += weight * get_rated_sector_representation(
                            model, table, evaluation_parameters[parameter])
                    elif evaluation_parameters[parameter] == \
                            'sector coupling supply':
                        sum_model += weight * get_rated_sector_supply(
                            model, table)
                    elif evaluation_parameters[parameter] == \
                            'sector coupling demand':
                        sum_model += weight * get_rated_sector_demand(
                            model, table)
                    elif evaluation_parameters[parameter] == \
                            'sector coupling storage':
                        sum_model += weight * get_rated_sector_storage(
                            model, table)
                    elif evaluation_parameters[parameter] == \
                            'decision making':
                        sum_model += weight * get_rated_decision(
                            model, table)
                    elif evaluation_parameters[parameter] == \
                            'grid representation':
                        sum_model += weight * get_rated_operation_repr_grid(
                            model, table)
            weighted_models[model][field] = sum_model / sum_weighting
    weighted_models_df = pd.DataFrame.from_dict(weighted_models).transpose()
    return weighted_models_df


def get_rated_sector_representation(name_model, table, sector,
                                    sum_representation=0):
    """
    Specific method to evaluate sector representation within a model

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sector: str
        Evaluated sector, currently only 'heat' and 'transport' are available
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if table.loc[name_model,
                 'end disaggregated {} tech'.format(sector)] == 1 and \
            table.loc[name_model,
                      'end disaggregated {} dem'.format(sector)] == 1:
        sum_representation += 1
    elif table.loc[name_model,
                   'end disaggregated {} tech'.format(sector)] == 1 or \
            table.loc[name_model,
                      'end disaggregated {} dem'.format(sector)] == 1:
        sum_representation += (2 / 3)
    elif table.loc[name_model, 'exo aggregated {} dem'.format(sector)] == 1:
        sum_representation += (1 / 3)
    elif table.loc[name_model, '{} sector excluded'.format(sector)] == 1:
        pass
    else:
        print('{} sector not specified for model {}.'.
              format(sector, name_model))
    if not pd.isnull(table.loc[name_model, 'other {} representation'.format(
            sector)]) and not \
            table.loc[name_model, 'other {} representation'.format(sector)] == 0:
        print('Other {} representation specified in model {}. '
              'Please check.'.format(sector, name_model))
    return sum_representation


def get_rated_sector_supply(name_model, table, sum_representation=0):
    """
    Specific method to evaluate supply representation within a model if supply
    side sector coupling technologies are represented in the model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if table.loc[name_model, 'CHP/pos'] == 1 or \
            table.loc[name_model, 'CHP/def'] == 1:
        if table.loc[name_model, 'minimum load yes'] == 1:
            sum_representation += 0.5
        if table.loc[name_model, 'discrete expansion yes'] == 1:
            sum_representation += 0.5
    else:
        pass
    return sum_representation


def get_rated_sector_storage(name_model, table, sum_representation=0):
    """
    Specific method to evaluate storage representation within a model if
    sector coupling storage technologies are represented in the model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if \
            table.loc[name_model, 'Fuels (H2)/def'] == 1 or \
            table.loc[name_model, 'Fuels (H2)/pos'] == 1 or \
            table.loc[name_model, 'Heat storage/pos'] == 1 or \
            table.loc[name_model, 'Heat storage/def'] == 1 or \
            table.loc[name_model, 'V2Grid/pos'] == 1 or \
            table.loc[name_model, 'V2Grid/def'] == 1:
        if table.loc[name_model, 'self discharge yes'] == 1.0:
            sum_representation += 1 / 3
        if table.loc[name_model, 'cycle aging'] == 1.0:
            sum_representation += 1 / 6
        if table.loc[name_model, 'calendrical aging'] == 1.0:
            sum_representation += 1 / 6
        if table.loc[name_model, 'dynamic'] == 1.0:
            sum_representation += 1 / 3
        elif table.loc[name_model, 'fixed/static'] == 1.0:
            sum_representation += 1 / 6
    else:
        pass
    return sum_representation


def get_rated_sector_demand(name_model, table, sum_representation=0):
    """
    Specific method to evaluate demand representation within a model if
    sector coupling demand technologies are represented in the model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if \
            table.loc[name_model, 'P2Gas/def'] == 1 or \
            table.loc[name_model, 'P2Gas/pos'] == 1 or \
            table.loc[name_model, 'P2H2/pos'] == 1 or \
            table.loc[name_model, 'P2H2/def'] == 1 or \
            table.loc[name_model, 'HP/pos'] == 1 or \
            table.loc[name_model, 'HP/def'] == 1 or \
            table.loc[name_model, 'EV/pos'] == 1 or \
            table.loc[name_model, 'EV/def'] == 1:
        if table.loc[name_model, 'shifting time yes'] == 1.0:
            sum_representation += 1 / 3
        if table.loc[name_model, 'price elasticity yes'] == 1.0:
            sum_representation += 1 / 3
        sum_representation += get_rated_operation_repr_max_def_load(
                    name_model, table) / 3
    else:
        pass
    return sum_representation


def get_rated_decision(name_model, table, sum_representation=0):
    """
    Specific method to evaluate decision making process within a model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if table.loc[name_model, 'perfect foresight'] == 1 and \
            table.loc[name_model, 'rolling horizon / myopic foresight'] == 1 and \
            table.loc[name_model, 'decision-/agentbased'] == 1:
        sum_representation += 1
    elif table.loc[name_model, 'decision-/agentbased'] == 1 and \
            table.loc[name_model, 'rolling horizon / myopic foresight'] == 1:
        sum_representation += 0.8
    elif table.loc[name_model, 'perfect foresight'] == 1 and \
            table.loc[name_model, 'rolling horizon / myopic foresight'] == 1:
        sum_representation += 0.6
    elif table.loc[name_model, 'perfect foresight'] == 1 and \
            table.loc[name_model, 'decision-/agentbased'] == 1:
        sum_representation += 0.6
    elif table.loc[name_model, 'decision-/agentbased'] == 1 or \
            table.loc[name_model,'rolling horizon / myopic foresight'] == 1:
        sum_representation += 0.4
    elif table.loc[name_model, 'perfect foresight'] == 1:
        sum_representation += 0.2
    elif table.loc[name_model, 'no decision making'] == 1 or \
            table.loc[name_model, 'other decision making']:
        pass
    else:
        print('Decision making not specified for model {}.'.
              format(name_model))
    return sum_representation


def get_rated_operation_repr_grid(name_model, table, sum_representation=0):
    """
    Specific method to evaluate grid representation within a model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if table.loc[name_model, 'AC PF'] == 1 and \
            table.loc[name_model, 'DC PF'] == 1 and \
            table.loc[name_model, 'interconnectors'] == 1 and \
            table.loc[name_model, 'transfer capacity'] == 1:
        sum_representation += 1
    elif table.loc[name_model, 'AC PF'] == 1 and \
            table.loc[name_model, 'DC PF'] == 1 and \
            table.loc[name_model, 'interconnectors'] == 1:
        sum_representation += 0.86
    elif table.loc[name_model, 'AC PF'] == 1 and \
            table.loc[name_model, 'DC PF'] == 1 and \
            table.loc[name_model, 'transfer capacity'] == 1:
        sum_representation += 0.71
    elif table.loc[name_model, 'DC PF'] == 1 and \
            table.loc[name_model, 'AC PF'] == 1:
        sum_representation += 0.57
    elif table.loc[name_model, 'AC PF'] == 1 and \
            table.loc[name_model, 'transfer capacity'] == 1:
        sum_representation += 0.43
    elif table.loc[name_model, 'DC PF'] == 1 and \
            table.loc[name_model, 'transfer capacity'] == 1:
        sum_representation += 0.43
    elif table.loc[name_model, 'DC PF'] == 1 or \
            table.loc[name_model, 'AC PF'] == 1:
        sum_representation += 0.28
    elif table.loc[name_model, 'transfer capacity'] == 1:
        sum_representation += 0.14
    elif table.loc[name_model, 'no grid'] == 1:
        pass
    else:
        print('Grid representation not specified for model {}.'.
              format(name_model))
    return sum_representation


def get_rated_operation_repr_max_def_load(name_model, table,
                                          sum_representation=0):
    """
    Specific method to evaluate representation of maximum deferrable load
    within a model.

    :param name_model: str
        name of the model
    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param sum_representation: float
        Sum of representation of previous calculations, defaults to 0
    :return:
    """
    if table.loc[name_model, 'time- and type-dependent'] == 1:
        sum_representation += 1
    elif table.loc[name_model, 'Type-dependent'] == 1:
        print('Model {} only ticked type-dependent. Please check.'.
              format(name_model))
    elif table.loc[name_model, 'Time-dependent'] == 1:
        sum_representation += (2 / 3)
    elif table.loc[name_model, 'max def load fixed value'] == 1:
        sum_representation += (1 / 3)
    elif table.loc[name_model, 'no max def load'] == 1:
        pass
    else:
        print('Model {} has not ticket any value for max def load.'.
              format(name_model))
    return sum_representation


def get_technology_representation_models_from_technology_dict(table,
                                                              technology_dict):
    """
    Method to check if certain technologies are possible to define or even
    predefined in the models present in inserted table.

    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param technology_dict: dict
        keys are the examined technology groups, e.g. flexibility categories
        entries are lists of the specific flexibility options for which the
        representation is to be checked, e.g. ['photovoltaic', 'wind onshore']
    :return: tuple of pd.DataFrame
        first includes the share of technologies in a model that is possible to
        represent, the second the share of technologies that is predefined
        within the examined models
    """
    models_pos = {}
    models_pred = {}
    for model in table.index:
        model_pos = {}
        model_pred = {}
        for tech, params in technology_dict.items():
            model_pos[tech], model_pred[tech] = \
                get_rated_tech_repr_by_name(table, model, params)
        models_pos[model] = model_pos
        models_pred[model] = model_pred
    models_pos_df = pd.DataFrame.from_dict(models_pos).transpose()
    models_pred_df = pd.DataFrame.from_dict(models_pred).transpose()
    return models_pos_df, models_pred_df


def get_rated_tech_repr_by_name(table, name_model, name_techs):
    """
    Method to evaluate if list of technologies is possible to implement or
    predefined in certain.

    :param table: pandas.DataFrame
        Index are entries of inserted list models
        Columns are evaluated parameters in the survey
    :param name_model: str
        name of the examined model
    :param name_techs:  list
        list of technologies to be examined
    :return: tuple of floats
        values will be between zero and one and display the share of examined
        technologies that can be implemented (first entry of tuple) or are
        even predefined (second entry of tuple) in the model

    """
    name_techs_pos = [tech + '/pos' for tech in name_techs]
    name_techs_pred = [tech + '/def' for tech in name_techs]
    tech_pos = table.loc[name_model, name_techs_pos]
    tech_pred = table.loc[name_model, name_techs_pred]
    rated_tech_representation_pos = tech_pos.sum() / len(name_techs)
    rated_tech_representation_pred = tech_pred.sum() / len(name_techs)
    return rated_tech_representation_pos, rated_tech_representation_pred

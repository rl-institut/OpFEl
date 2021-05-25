__copyright__ = "Reiner Lemoine Institut gGmbH"
__license__   = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__       = "https://github.com/rl-institut/OpFEl/blob/master/LICENSE"
__author__    = "AnyaHe, ricrei, a-linke"


import os
from pathlib import Path
import pandas as pd
module_path = os.path.abspath(os.path.join('.'))

from tools import tools
from tools.plots import plot_representation_single, plot_representation_triple,\
    plot_representation_holistic, plot_boxplot, plot_bar_horizontal


# # General characteristics

cur_dir = Path(os.getcwd())
table_values = pd.read_csv(os.path.join(cur_dir,'data/Evaluation_Table.csv'),
                           sep=";").set_index('Model / framework').fillna(0)
nr_of_surveys = len(table_values)


spatial_scope = \
    table_values.loc[:, 'local (NUTS3)/pos':'other spatial scope'].sum()
spatial_scope['other spatial scope/pos'] = \
    len(table_values['other spatial scope'].to_numpy().nonzero()[0])
spatial_scope['other spatial scope/used'] = \
    len(table_values['other spatial scope'].to_numpy().nonzero()[0])

plot_bar_horizontal(
    spatial_scope, ['Local', 'Regional', 'National', 'International', 'Other'],
    title='Spatial Scope', max_val=nr_of_surveys, no_label=True,
    save_fig_dir=module_path + '/plots/01a_paper_spatial_scope.pdf')

print(table_values['other spatial scope'])

temporal_scope = \
    table_values.loc[:, 'very short/pos':'other temporal scope'].sum()
temporal_scope['other temporal scope/pos'] = \
    len(table_values['other temporal scope'].to_numpy().nonzero()[0])
temporal_scope['other temporal scope/used'] = \
    len(table_values['other temporal scope'].to_numpy().nonzero()[0])

plot_bar_horizontal(
    temporal_scope, ['Very Short', 'Short', 'Intermediate', 
                     'Long', 'Other'], title='Temporal Scope',
    max_val=nr_of_surveys, no_label=True,
    save_fig_dir=module_path + '/plots/01b_paper_temporal_scope.pdf')


print(table_values['other temporal scope'])

temporal_resolution = \
    table_values.loc[:, '<hourly/pos':'other temporal resolution'].sum()
temporal_resolution['other temporal resolution/pos'] = \
    len(table_values['other temporal resolution'].to_numpy().nonzero()[0])
temporal_resolution['other temporal resolution/used'] = \
    len(table_values['other temporal resolution'].to_numpy().nonzero()[0])

plot_bar_horizontal(
    temporal_resolution,
    ['< Hourly', 'Hourly', 'Intermediate', 'Annual', 'Other\nResolution'],
    title='Temporal Resolution', max_val=nr_of_surveys, figsize=(4., 2.5),
    save_fig_dir=module_path + '/plots/01c_paper_temporal_resolution.pdf')

print(table_values['other temporal resolution'])


# # Evaluation of flexibility representation 

models = table_values.index


# **Definition of fulfillment criteria. Further described in methodology.**

evaluation_parameters = tools.default_evaluation_parameters()


# ## Supply representation

parameters_with_weights_supply = {
    'Technology\nRepresentation':
        {'coal': 1, 'lignite': 1, 'oil': 1, 'natural gas': 1, 'CCGT': 1,
         'OCGT': 1, 'bioenergy': 1, 'Hydro reservoir': 1, 'geothermal energy': 1,
         'concentrated solar': 1, 'photovoltaic': 1, 'wind onshore': 1,
         'wind offshore': 1, 'river hydro': 1, 'wave power': 1, 'tidal power': 1,
         'PEM-FC': 1, 'SOFC': 1, 'nuclear': 1},
    'Detailed\nCharacteristics':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1,
         'discrete capacity expansion': 1, 'curtailed operation': 1,
         'minimum load': 1}
}


weighted_models_supply_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_supply, evaluation_parameters, table_values)

rating_supply = weighted_models_supply_df.sum(axis=1).divide(2)
rating_supply.sort_values(ascending=False)*100

# Plot all models
plot_representation_single(
    weighted_models_supply_df.loc[
        rating_supply.sort_values(ascending=False).index], 'Supply')


# ### Detailed Evaluation

parameters_with_weights_supply_tech = {
    'Conventional':
        {'coal': 1, 'lignite': 1, 'oil': 1, 'natural gas': 1, 'CCGT': 1,
         'OCGT': 1, 'nuclear': 1},
    'Dispatchable\nRES':
        {'bioenergy': 1, 'Hydro reservoir': 1, 'geothermal energy': 1,
         'concentrated solar': 1},
    'Variable\nRES':
        {'photovoltaic': 1, 'wind onshore': 1, 'wind offshore': 1,
         'river hydro': 1, 'wave power': 1, 'tidal power': 1},
    'Fuel Cells':
        {'PEM-FC': 1, 'SOFC': 1}
}

parameters_with_weights_supply_char = {
    'Technology\nSpecifications':
        {'curtailed operation': 1, 'minimum load': 1},
    'Operations':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1},
    'Discrete\nExpansion':
        {'discrete capacity expansion': 1,}
}

weighted_models_supply_tech_df = \
    tools.get_weighted_models_from_evaluation_dicts(
        models, parameters_with_weights_supply_tech, evaluation_parameters,
        table_values)
weighted_models_supply_char_df = \
    tools.get_weighted_models_from_evaluation_dicts(
        models, parameters_with_weights_supply_char, evaluation_parameters,
        table_values)

rating_supply_df = \
    pd.DataFrame(rating_supply.sort_values(ascending=False)).rename(
        columns={0:'Overall\nRating'})
plot_representation_triple(
    rating_supply_df, weighted_models_supply_tech_df[
        parameters_with_weights_supply_tech.keys()].loc[
        rating_supply.sort_values(ascending=False).index], 
    weighted_models_supply_char_df[parameters_with_weights_supply_char.keys()].loc[
        rating_supply.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/02_supply.pdf' )

plot_representation_triple(
    rating_supply_df, weighted_models_supply_tech_df[
        parameters_with_weights_supply_tech.keys()].loc[
        rating_supply.sort_values(ascending=False).index],
    weighted_models_supply_char_df[
        parameters_with_weights_supply_char.keys()].loc[
        rating_supply.sort_values(ascending=False).index], figsize=(6.5, 4.8))


# ## Demand representation

# Demand dict
parameters_with_weights_demand = {
    'Technology\nRepresentation':
        {'households': 1, 'industrial load': 1, 'service sector': 1},
    'Detailed\nCharacteristics':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1,
         'maximum deferrable load': 1, 'shifting time': 1, 'price elasticity': 1}
}

weighted_models_demand_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_demand, evaluation_parameters, table_values)
rating_demand = weighted_models_demand_df.sum(axis=1).divide(2)
rating_demand.sort_values(ascending=False)*100

# Plot all models
plot_representation_single(
    weighted_models_demand_df.loc[
        rating_demand.sort_values(ascending=False).index], 'Demand')


# ### Detailed Evaluation

# Demand dict
parameters_with_weights_demand_tech = {
    'Household': {'households': 1}, 
    'Industry': {'industrial load': 1}, 
    'Service': {'service sector': 1}}
parameters_with_weights_demand_char = {
    'Technology\nSpecifications':
        {'maximum deferrable load': 1, 'shifting time': 1},
    'Operations':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1},
    'Price\nElasticity':
        {'price elasticity': 1}
}

weighted_models_demand_tech_df = \
    tools.get_weighted_models_from_evaluation_dicts(
        models, parameters_with_weights_demand_tech, evaluation_parameters,
        table_values)
weighted_models_demand_char_df = \
    tools.get_weighted_models_from_evaluation_dicts(
        models, parameters_with_weights_demand_char, evaluation_parameters,
        table_values)

# plot all dual
rating_demand_df = pd.DataFrame(
    rating_demand.sort_values(ascending=False)).rename(columns={0:'Overall\nRating'})
plot_representation_triple(rating_demand_df,
    weighted_models_demand_tech_df[parameters_with_weights_demand_tech.keys()].loc[
        rating_demand.sort_values(ascending=False).index], 
    weighted_models_demand_char_df[parameters_with_weights_demand_char.keys()].loc[
        rating_demand.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/03_demand.pdf')


# ## Storage representation

# Storage dict
parameters_with_weights_storage = {
    'Technology\nRepresentation':
        {'Batteries': 1,  'PHS': 1, 'CAES': 1, 'Caps': 1, 'Flywheels': 1},
    'Detailed\nCharacteristics':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1,
         'storage implementation': 1, 'aging': 1, 'self discharge': 1}
}

weighted_models_storage_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_storage, evaluation_parameters, table_values)
rating_storage = weighted_models_storage_df.sum(axis=1).divide(2)
rating_storage.sort_values(ascending=False)*100

# Plot all models
plot_representation_single(
    weighted_models_storage_df.loc[
        rating_storage.sort_values(ascending=False).index], 'Storage')


# ### Detailed Evaluation

# Storage dict
parameters_with_weights_storage_tech = {
    'Long-term': {'PHS': 1, 'CAES': 1}, 
    'Medium-term': {'Batteries': 1},  
    'Short-term': {'Caps': 1, 'Flywheels': 1},}
parameters_with_weights_storage_char = {
    'Technology\nSpecifications': {'aging': 1, 'self discharge': 1}, 
    'Storage\nImplementation': {'storage implementation': 1},
    'Operations': {'efficiency': 1, 'ramping': 1, 'response time': 1,
                   'recovery time': 1}
}

weighted_models_storage_tech_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_storage_tech, evaluation_parameters, table_values)
weighted_models_storage_char_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_storage_char, evaluation_parameters, table_values)


# plot all dual
rating_storage_df = \
    pd.DataFrame(rating_storage.sort_values(ascending=False)).rename(
        columns={0:'Overall\nRating'})
plot_representation_triple(
    rating_storage_df, weighted_models_storage_tech_df[
        parameters_with_weights_storage_tech.keys()].loc[
        rating_storage.sort_values(ascending=False).index], 
    weighted_models_storage_char_df[parameters_with_weights_storage_char.keys()].loc[
        rating_storage.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/04_storage.pdf')


# ## Sector coupling representation

# Sector coupling dict
parameters_with_weights_sector = {
    'Technology\nRepresentation': {
        'P2H2': 1, 'HP': 1, 'EV': 1, 'Fuels': 1, 'Heat storage': 1,
        'V2G': 1, 'CHP': 1},
    'Detailed\nCharacteristics':
        {'efficiency': 1, 'ramping': 1, 'response time': 1, 'recovery time': 1,
         'Heat': 1, 'Transport': 1, 'sector coupling supply': 1,
         'sector coupling demand': 1, 'sector coupling storage': 1},
}

weighted_models_sector_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_sector, evaluation_parameters, table_values)
rating_sector = weighted_models_sector_df.sum(axis=1).divide(2)
rating_sector.sort_values(ascending=False)*100

# Plot all models
plot_representation_single(
    weighted_models_sector_df.loc[
        rating_sector.sort_values(ascending=False).index], 'Sector Coupling')


# ### Detailed Evaluation

# Sector coupling dict
parameters_with_weights_sector_tech = {
    'Supply\nTechnology': {'CHP': 1},
    'Demand\nTechnology': {'P2H2': 1, 'HP': 1, 'EV': 1}, #P2H2 represents P2G here
    'Storage\nTechnology': {'Fuels': 1, 'Heat storage': 1, 'V2G': 1, }, }
parameters_with_weights_sector_char = {
    'Sector\nRepresentation': {'Heat': 1, 'Transport': 1},
    'Technology\nSpecifications':
        {'sector coupling supply': 1, 'sector coupling demand': 1,
         'sector coupling storage': 1},
    'Operations': {'efficiency': 1, 'ramping': 1, 'response time': 1,
                   'recovery time': 1}
}

weighted_models_sector_tech_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_sector_tech, evaluation_parameters, table_values)
weighted_models_sector_char_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_sector_char, evaluation_parameters, table_values)

# plot all dual
rating_sector_df = \
    pd.DataFrame(rating_sector.sort_values(ascending=False)).rename(
        columns={0:'Overall\nRating'})
plot_representation_triple(rating_sector_df, 
    weighted_models_sector_tech_df[parameters_with_weights_sector_tech.keys()].loc[
        rating_sector.sort_values(ascending=False).index], 
    weighted_models_sector_char_df[parameters_with_weights_sector_char.keys()].loc[
        rating_sector.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/05_sector.pdf')


# ## Network representation

# Network dict
parameters_with_weights_network = {
    'Technology\nRepresentation':
        {'Distribution Grid': 1, 'Transmission Grid': 1, #'Smart Grid': 1, 'Microgrid': 1, 'interconnectors': 1
         'network extension': 1, 'switches': 1},
    'Detailed\nCharacteristics':
        {'Grid representation': 1, 'import': 1,
                'grid ancillary services': 1}

}

weighted_models_network_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_network, evaluation_parameters, table_values)
rating_network = weighted_models_network_df.sum(axis=1).divide(2)
rating_network.sort_values(ascending=False)*100

# Plot all models
plot_representation_single(
    weighted_models_network_df.loc[
        rating_network.sort_values(ascending=False).index], 'Network')


# ### Detailed Evaluation

# Network dict
parameters_with_weights_network_tech = {
    'Grid Types':
        {'Distribution Grid': 1, 'Transmission Grid': 1},
    'Topology': {'network extension': 1, 'switches': 1},}
parameters_with_weights_network_char = {
    'Grid\nRepresen-\ntation':{'Grid representation': 1}, 
    'Import\nExport':{'import': 1},
    'Ancillary\nServices':{'grid ancillary services': 1}

}

weighted_models_network_tech_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_network_tech, evaluation_parameters, table_values)
weighted_models_network_char_df = tools.get_weighted_models_from_evaluation_dicts(
    models, parameters_with_weights_network_char, evaluation_parameters, table_values)

# plot all dual
rating_network_df = \
    pd.DataFrame(rating_network.sort_values(ascending=False)).rename(
        columns={0:'Overall\nRating'})
plot_representation_triple(rating_network_df, 
    weighted_models_network_tech_df[parameters_with_weights_network_tech.keys()].loc[
        rating_network.sort_values(ascending=False).index], 
    weighted_models_network_char_df[parameters_with_weights_network_char.keys()].loc[
        rating_network.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/06_network.pdf')


# ## Holistic representation

# Holistic definition is the concatenated version of all ratings

weighted_models_holistic_df = pd.concat([rating_supply_df.rename(
    columns={'Overall\nRating':'Supply'}),
    rating_demand_df.rename(columns={'Overall\nRating':'Demand'}),
    rating_storage_df.rename(columns={'Overall\nRating':'Storage'}),
    rating_network_df.rename(columns={'Overall\nRating':'Network'}),
    rating_sector_df.rename(columns={'Overall\nRating':'Sector\nCoupling'})],
    sort=True, axis=1)
rating_holistic = weighted_models_holistic_df.sum(axis=1).divide(5)
rating_holistic.sort_values(ascending=False)*100

# Plot all models
rating_holistic_df = \
    pd.DataFrame(rating_holistic.sort_values(ascending=False)).rename(
        columns={0:'Overall\nRating'})
plot_representation_holistic(
    rating_holistic_df, weighted_models_holistic_df.loc[
        rating_holistic.sort_values(ascending=False).index], figsize=(6.5,4.8),
    save_fig_dir=module_path + '/plots/07_holistic.pdf')


print(weighted_models_holistic_df.loc[
        rating_holistic.sort_values(ascending=False).index])

plot_boxplot(weighted_models_holistic_df.transpose(),
             save_fig=module_path + '/plots/08_boxplot.pdf')

threshold = 0.7

high_representation_supply = \
    rating_supply_df[rating_supply_df > threshold].dropna()
high_representation_demand = \
    rating_demand_df[rating_demand_df > threshold].dropna()
high_representation_storage = \
    rating_storage_df[rating_storage_df > threshold].dropna()
high_representation_network = \
    rating_network_df[rating_network_df > threshold].dropna()
high_representation_sector = \
    rating_sector_df[rating_sector_df > threshold].dropna()

high_representation_df = \
    pd.concat([high_representation_supply, high_representation_demand,
               high_representation_storage, high_representation_network,
               high_representation_sector], axis=1, sort=False)

high_representation_df.columns = ['Supply', 'Demand', 'Storage', 'Network',
                                  'Sector coupling']

print(high_representation_df)

# #Appendix

generalfactors = table_values.loc[:, ['prob yes', 'social yes']].sum()
plot_bar_horizontal(
        generalfactors, ['Probalistic\nBehavior', 'Social\nFactors'],
        title='General Factors', max_val=nr_of_surveys, figsize=(3., 2.5),
    save_fig_dir=module_path + '/plots/a00a_paper_general_factors.pdf')


decisionmaking = \
    table_values.loc[:, 'perfect foresight':'other decision making'].sum()
decisionmaking['other decision making'] = \
    len(table_values['other decision making'].to_numpy().nonzero()[0])
decisionmaking['no decision making'] = \
    table_values.loc[:, 'no decision making'].sum()
plot_bar_horizontal(
    decisionmaking, ['Perfect Foresight','Rolling Horizon /\nMyopic Foresight',
                     'Decision- /\nAgentbased', 'Other Decision\nMaking',
                     'No Decision\nMaking'],
    title='Decision Making Process', max_val=nr_of_surveys,
    save_fig_dir=module_path + '/plots/a00b_paper_decision_making.pdf')

print(table_values['other decision making'])

flex_specs = \
    table_values.loc[
    :, ['efficiency fixed value', 'efficiency function',
        'ramping yes', 'response time yes', 'recovery time yes']].sum()
plot_bar_horizontal(
    flex_specs, ['Fixed Efficiency', 'Dynamic Efficiency', 'Ramping',
                 'Response Time', 'Recovery Time'],
    title='Flexibility Specifications', max_val=nr_of_surveys, figsize=(3.5, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a00c_paper_flex_spec.pdf')

# plot which supply technologies are represented to what extent
convPP = table_values.loc[:, 'hard coal/pos':'OCGT/def'].sum()
dispRES = \
    table_values.loc[:, 'Bioenergy/pos':'concentrated solar power/def'].sum()
vRES = table_values.loc[:, 'photovoltaic/pos':'tidal power/def'].sum()
other_supply = table_values.loc[:, 'PEM-FC/pos':'Nuclear/def'].sum()

supply = pd.concat([convPP, dispRES, vRES, other_supply])

plot_bar_horizontal(
    series=supply,
    x_labels=['Hard Coal', 'Lignite', 'Oil', 'Natural Gas',
              'CCGT', 'OCGT', 'Bioenergy', 'Geothermal',
              'Hydro Reservoir', 'CSP', 'PV', 'Wind Onshore',
              'Wind Offshore', 'Hydro ROR', 'Wave', 'Tidal',
              'PEM-FC', 'SOFC', 'Nuclear'],
    title='Supply Technologies', max_val=nr_of_surveys,
    label_name = 'pos_def', figsize=(3.5, 3.75), bbox_to_anchor=(-0.4,0.),
    save_fig_dir=str(cur_dir) + '/plots/a01a_paper_supply_tech.pdf')

tech_representation = \
    table_values.loc[:, ['minimum load yes', 'discrete expansion yes',
                         'curtailed operation yes']].sum()
plot_bar_horizontal(
    tech_representation, ['Minimum\nLoad', 'Discrete\nExpansaion',
                              'Curtailed\nOperation'],
    title='Supply Specifications', max_val=nr_of_surveys, figsize=(3, 2.5),
    save_fig_dir=str(cur_dir) + '/plots/a01b_paper_supply_spec.pdf')

# plot which demand technologies are represented to what extent
demand = table_values.loc[:, 'households/pos':'service sector/def'].sum()

plot_bar_horizontal(
    series=demand, x_labels=['Households', 'Industrial', 'Service'],
    title='Demand Technologies', max_val=nr_of_surveys, label_name='pos_def',
    bbox_to_anchor=(-0.4, 0.),
    save_fig_dir=str(cur_dir) + '/plots/a02a_paper_demand_tech.pdf')

# plot only highest rated options
tmp_tech_representation_demand = \
    pd.concat([table_values.loc[:, 'max def load fixed value': 'no max def load'],
               table_values.loc[:, ['shifting time yes']]], axis=1)
tmp_tech_representation_demand['max def load fixed value'] = \
    tmp_tech_representation_demand['max def load fixed value'] * \
    (1-tmp_tech_representation_demand['time- and type-dependent']) * \
    (1-tmp_tech_representation_demand['Time-dependent']) * \
    (1-tmp_tech_representation_demand['Type-dependent'])
tmp_tech_representation_demand['Time-dependent'] = \
    tmp_tech_representation_demand['Time-dependent'] * \
    (1-tmp_tech_representation_demand['time- and type-dependent'])
tmp_tech_representation_demand['Type-dependent'] = \
    tmp_tech_representation_demand['Type-dependent'] * \
    (1-tmp_tech_representation_demand['time- and type-dependent'])

tech_representation_demand = tmp_tech_representation_demand.sum()
plot_bar_horizontal(
    tech_representation_demand,
    ['Fixed Value MDL', 'Time-Dependent MDL', 'Type-Dependent MDL',
     'Time- & Type-\nDependent MDL', 'No MDL', 'Shifting Time'],
    title='Demand Specifications', max_val=nr_of_surveys, figsize=(3.25, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a02b_paper_demand_spec.pdf')

# plot which storage technologies are represented to what extent
storage = table_values.loc[:, 'PHS/pos':'Flywheels/def'].sum()

plot_bar_horizontal(
    series=storage, x_labels=[
        'Pumped Hydro', 'Batteries', 'Compressed Air', 'Capacitors',
        'Flywheels'], title='Storage Technologies', max_val=nr_of_surveys,
    label_name='pos_def', bbox_to_anchor=(-0.4, 0.),
    save_fig_dir=str(cur_dir) + '/plots/a03a_paper_storage_tech.pdf')

# plot only highest rated options
tmp_tech_representation_storage = \
    table_values.loc[:, ['fixed/static', 'dynamic', 'cycle aging',
                         'calendrical aging', 'self discharge yes']]
tmp_tech_representation_storage['fixed/static'] = \
    tmp_tech_representation_storage['fixed/static'] * \
    (1-tmp_tech_representation_storage['dynamic'])

tech_representation_storage = tmp_tech_representation_storage.sum()

plot_bar_horizontal(
    tech_representation_storage,
    ['Fixed Model', 'Dynamic\nModel', 'Cycle Aging', 'Calendrical\nAging',
     'Self Discharge'], title='Storage Specifications', max_val=nr_of_surveys,
    figsize=(3.25, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a03b_paper_storage_spec.pdf')

# plot which network technologies are represented to what extent
network = table_values.loc[:, ['Distribution Grid/pos', 'Distribution Grid/def',
                               'Transmission Grid/pos', 'Transmission Grid/def',
                              'interconnectors/pos', 'interconnectors/def',
                              'network extension/pos', 'network extension/def',
                               'switches/pos', 'switches/def']].sum()

plot_bar_horizontal(
    series=network,
    x_labels=['Distribution\nGrid', 'Transmission\nGrid', 'Interconnectors',
              'Network\nExtension', 'Switches'], title='Network Technologies',
    max_val=nr_of_surveys, label_name = 'pos_def', bbox_to_anchor=(-0.4, 0.),
    save_fig_dir=str(cur_dir) + '/plots/a04a_paper_network_tech.pdf')

ancillary_services = \
    table_values.loc[:, 'spinning reserve':'black start' ].sum()
plot_bar_horizontal(
    ancillary_services,
    ['Spinning Reserve', 'Balancing Energy', 'Sheddable Loads',
     'Feed-in Management', 'Redispatch', 'Power Factor Correction',
     'Curtailment', 'Blackstart'], title='Ancillary Services',
    max_val=nr_of_surveys,
    save_fig_dir=str(cur_dir) + '/plots/a04b_ancillary_services.pdf')

tech_representation_network = \
    table_values.loc[:, ['transfer capacity', 'AC PF', 'DC PF',
                         'simplified', 'flow based', 'other import']].sum()

plot_bar_horizontal(
    tech_representation_network,
    ['NTC', 'AC PF', 'DC PF', 'Simplified Im-/Export', 'Flow-Based Im-/Export'],
    title='Network Specifications', max_val=nr_of_surveys, figsize=(3.5, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a04c_paper_network_spec.pdf')

# plot which sector coupling technologies are represented to what extent
sector = table_values.loc[:, ['P2Gas/pos', 'P2Gas/def',
                               'Fuels (H2)/pos', 'Fuels (H2)/def',
                              'CHP/pos', 'CHP/def',
                              'HP/pos', 'HP/def',
                              'Heat storage/pos', 'Heat storage/def',
                               'EV/pos', 'EV/def', 'V2Grid/pos', 'V2Grid/def']].sum()

plot_bar_horizontal(
    series=sector, title='SC Technologies', max_val=nr_of_surveys,
    x_labels=['Power-to-Gas', 'Fuels', 'CHP', 'Heat Pumps', 'Heat Storage',
              'Electric Vehicles', 'Vehicle-to-Grid'], label_name='pos_def',
    bbox_to_anchor=(-0.4,0.),
    save_fig_dir=str(cur_dir) + '/plots/a05a_paper_sector_tech.pdf')

tech_representation_heat = table_values.loc[:, 'heat sector excluded':'transport sector excluded'].sum()

plot_bar_horizontal(
    tech_representation_heat,
    ['Excluded', 'Exogen Aggregated', 'Endogen Demand', 'Endogen Technology',
     'Other'], title='Heat Specifications', max_val=nr_of_surveys,
    figsize=(3.5, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a05b_paper_heat_spec.pdf')

tech_representation_transport = \
    table_values.loc[:, 'transport sector excluded':'prob yes'].sum()

plot_bar_horizontal(
    tech_representation_transport,
    ['Excluded', 'Exogen Aggregated', 'Endogen Demand', 'Endogen Technology',
     'Other'], title='Transport Specifications', max_val=nr_of_surveys,
    figsize=(3.5, 2.4),
    save_fig_dir=str(cur_dir) + '/plots/a05c_paper_transport_spec.pdf')

print('SUCCESS.')
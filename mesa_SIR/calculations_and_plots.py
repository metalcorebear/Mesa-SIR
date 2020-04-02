
import numpy as np
from datetime import date as datemethod
from datetime import datetime
import matplotlib.pyplot as plt
import os


''''
example of data collection function: 

m is variable for model
c_p is import calaculations_and_plots

Example DataCollector function
self.datacollector = DataCollector(model_reporters={"infected": lambda m: c_p.compute(m,'infected'),
                                                            "recovered": lambda m: c_p.compute(m,'recovered'),
                                                            "susceptible": lambda m: c_p.compute(m,"susceptible"),
                                                            "dead": lambda m: c_p.compute(m, "dead"),
                                                            "R0": lambda m: c_p.compute(m, "R0"),
                                                            "severe_cases": lambda m: c_p.compute(m,"severe")})
                                                            
   
Plots:

plot_SIR parameters: datacollection dataframe from get_model_vars_dataframe(); outputpath
plot_R0 parameters: datacollection dataframe get_model_vars_dataframe(); outputpath
plot_severe parameters: datacollection dataframe get_model_vars_dataframe(); outputpath
'''

# Compute SIR and dead at any point in time
def compute(model, report):
    total = 0
    if report == "R0":
        induced_infections = [a.induced_infections for a in model.schedule.agents if a.infected_others == True]
        if len(induced_infections) == 0:
            induced_infections = [0]
        # induced_infections_ = [value for value in induced_infections if value != 0]
        infection_array = np.array(induced_infections)
        R0 = np.average(infection_array)
        return R0
    elif report == "dead":
        total_dead = float(model.population - len(model.schedule.agents))
        return total_dead
    else:
        for a in model.schedule.agents:
            if getattr(a, report) == True:
                total += 1
        return total





# Plot output
def save_data(output_data, output_path = None, filename = "SIR_datafile.csv"):

    if output_path != None:
        output_file = os.path.join(output_path, filename)
        output_data.to_csv(output_file, encoding = "UTF8")
    else:
        output_data.to_csv(filename, encoding="UTF8")


# Plot output
def plot_SIR(df_out, title, output_path = None):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'SIR_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if (column != 'R0') and (column != 'severe_cases'):
            ax.plot(df_out[column], label=column)
    plt.title(title +' - SIR')
    plt.xlabel('Day')
    plt.ylabel('Population')
    ax.legend()
    if output_path != None:
        plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    else:
        plt.savefig(plot_name, dpi=300)
    plt.close()


def plot_R0(df_out, title, output_path = None):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'R0_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'R0':
            ax.plot(df_out[column], label=column)
    plt.title(title + ' - R0')
    plt.xlabel('Day')
    plt.ylabel('R0')
    ax.legend()
    if output_path != None:
        plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    else:
        plt.savefig(plot_name, dpi = 300)
    plt.close()


def plot_severe(df_out, title, output_path =None):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'Severe_Cases_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'severe_cases':
            ax.plot(df_out[column], label=column)
    plt.title(title + ' - Severe Cases')
    plt.xlabel('Day')
    plt.ylabel('Number of Severe Cases')
    ax.legend()
    if output_path != None:
        plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    else:
        plt.savefig(plot_name, dpi = 300)
    plt.close()

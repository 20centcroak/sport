import logging
import math
import plotly.express as px

from pandas import DataFrame
from pycroaktools.applauncher import Configuration


def convertMinSec(velocity: str):
    split = velocity.split(':')
    if len(split) < 2:
        raise ValueError("velocity should be given as min:sec")
    mins = float(split[0])
    secs = float(split[1])
    return 60/(mins+secs/60)


def invertConvertMinSec(velocity: float):
    logging.info('convert velocity {}'.format(velocity))
    allure = 60/velocity
    mins = int(allure)
    secs = int((allure - mins)*60)
    secs = str(secs) if len(str(secs)) == 2 else '0'+str(secs)
    logging.info(str(mins)+":"+str(secs))
    return str(mins)+":"+str(secs)


if __name__ == "__main__":
    settings = Configuration().settings(__file__)

    vma = convertMinSec(settings['vma'])
    logging.info('vma={} km/h'.format(vma))

    fcreserve = settings['fcmax']-settings['fcrepos']

    fczones = ["échauffement/récupération", "échauffement/récupération", "confort/endurance fondamentale", "confort/endurance fondamentale",
               "endurance active", "endurance active", "résistance", "résistance", "résistance dure", "résistance dure"]

    fcpercent = ["50%", "60%", "60%", "70%",
                 "70%", "80%", "80%", "90%", "90%", "100%"]

    fcvalues = [0.5*fcreserve + settings['fcrepos'], 0.6*fcreserve+settings['fcrepos'], 0.6*fcreserve+settings['fcrepos'], 0.7*fcreserve+settings['fcrepos'], 0.7*fcreserve +
                settings['fcrepos'], 0.8*fcreserve+settings['fcrepos'], 0.8*fcreserve+settings['fcrepos'], 0.9*fcreserve+settings['fcrepos'], 0.9*fcreserve+settings['fcrepos'], settings['fcmax']]
    df = DataFrame(data={"zone": fczones, "fc": fcvalues, "percentage": fcpercent})

    fig = px.bar_polar(df, r="fc", theta="zone", color="percentage", template="plotly_dark", hover_name='percentage',
                       color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig.show()

    work = ["échauffement/récupération", "échauffement/récupération", "échauffement/récupération", "endurance continue facile", "continue - gain endurance élevé",
            "continue - gain endurance très élevé - gain vma faible", "intermittente - gain endurance élevé - gain vma moyen", "intermittente - gain endurance moyen - gain vma élevé",
            "intermittente - gain vma très élevé", "intermittente - gain vma très élevé", "intermittente - gain vma très élevé"]

    vmapercent = ["60%", "65%", "70%", "75%", "80%",
                  "85%", "90%", "95%", "100%", "105%", "110%"]

    vmavalues = [0.6*vma, 0.65*vma, 0.7*vma, 0.75*vma, 0.8*vma,
                 0.85*vma, 0.9*vma, 0.95*vma, vma, 1.05*vma, 1.1*vma]

    vmaminsec = [invertConvertMinSec(value) for value in vmavalues ]

    df = DataFrame(data={"work": work, "kmh": vmavalues, "vma": vmaminsec, "percentage": vmapercent})

    fig = px.bar_polar(df, r="vma", theta="work", color="kmh", template="plotly_dark", hover_name='percentage',
                       color_discrete_sequence=px.colors.sequential.Plasma_r)

    fig.show()

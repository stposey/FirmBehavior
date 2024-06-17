
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'FirmBehaviorSignal'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 5
    MAXIMUM_PRICE = cu(100)
    MAXIMUM_QUALITY = 100
    INFORMAL_SIGNAL = 100
    FORMAL_SIGNAL = 1
    INSTRUCTIONS_TEMPLATE = 'FirmBehaviorSignal/instructions.html'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    profit = models.FloatField()
    quality1 = models.FloatField()
    quality2 = models.FloatField()
    quality3 = models.FloatField()
    quality4 = models.FloatField()
    quality5 = models.FloatField()
    price1 = models.FloatField()
    price2 = models.FloatField()
    price3 = models.FloatField()
    price4 = models.FloatField()
    price5 = models.FloatField()
    IS1 = models.FloatField()
    IS2 = models.FloatField()
    IS3 = models.FloatField()
    IS4 = models.FloatField()
    IS5 = models.FloatField()
    profit2 = models.FloatField()
    profit3 = models.FloatField()
    profit4 = models.FloatField()
    profit5 = models.FloatField()
    profit1 = models.FloatField()
    FS1 = models.FloatField()
    FS2 = models.FloatField()
    FS3 = models.FloatField()
    FS4 = models.FloatField()
    FS5 = models.FloatField()
def set_payoffs(group: Group):
    import pandas as pd
    import numpy as np
    
    qualities=[]
    prices=[]
    informalSignals=[]
    formalSignals=[]
    playerList=[]
    players = group.get_players()
    for p in players:
        if p.formalSignal==None:
            p.formalSignal= int(0)
    
    for p in players:
        qualities.append(p.quality)
        prices.append(p.price)
        formalSignals.append(p.formalSignal)
        informalSignals.append(p.informalSignal)
        playerList.append(p.id_in_group)
        p.perceivedQuality=p.quality+np.log(p.informalSignal+1)+50*p.formalSignal
    
    
    PlayerDF = pd.DataFrame(data = {'playerid':playerList,'quality':qualities,'price':prices,'informalSignal':informalSignals,'formalSignal':formalSignals})
    PlayerDF['perceivedQuality']=PlayerDF.quality+np.log(PlayerDF.informalSignal+1)+50*PlayerDF.formalSignal
    playerRank = PlayerDF.sort_values(by = ['perceivedQuality'])
    playerRank['QualityRank']=playerList
    playerRank.index=playerRank['QualityRank']
    
    
    demand1=((playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1]))-(playerRank.price[1]/playerRank.perceivedQuality[1])
    
    demand2=((playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2]))-(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1])
    
    demand3=((playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3]))-(playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2])
    demand4=((playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4]))-(playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3])
    demand5=1-(playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4])
    if demand1<0:
        demand1=0
    if demand2<0:
        demand2=0
    if demand3<0:
        demand3=0
    if demand4<0:
        demand4=0
    if demand5<0:
        demand5=0
    
    
    playerRank['demand']=[demand1,demand2,demand3,demand4,demand5]
    playerRank['profit']= playerRank.price*playerRank.demand-(playerRank.quality+.5*playerRank.informalSignal+playerRank.formalSignal*10)*playerRank.demand
    playersDF= playerRank.sort_values(by = ['playerid'])
    playersDF.index=playersDF['playerid']
    
    for p in players:
        if p.id_in_group==1:
            p.Demand=playersDF.demand[1]
        if p.id_in_group==2:
            p.Demand=playersDF.demand[2]
        if p.id_in_group==3:
            p.Demand=playersDF.demand[3]
        if p.id_in_group==4:
            p.Demand=playersDF.demand[4]
        if p.id_in_group==5:
            p.Demand=playersDF.demand[5]   
    
    for p in players:
        p.profit=(p.price-p.Cost)*p.Demand
    
    group.price1=round(playersDF.price[1],2)
    group.price2=round(playersDF.price[2],2)
    group.price3=round(playersDF.price[3],2)
    group.price4=round(playersDF.price[4],2)
    group.price5=round(playersDF.price[5],2)
    group.profit1=round(playersDF.profit[1],2)
    group.profit2=round(playersDF.profit[2],2)
    group.profit3=round(playersDF.profit[3],2)
    group.profit4=round(playersDF.profit[4],2)
    group.profit5=round(playersDF.profit[5],2)
    group.quality1=playersDF.quality[1]
    group.quality2=playersDF.quality[2]
    group.quality3=playersDF.quality[3]
    group.quality4=playersDF.quality[4]
    group.quality5=playersDF.quality[5]
    group.IS1=playersDF.informalSignal[1]
    group.IS2=playersDF.informalSignal[2]
    group.IS3=playersDF.informalSignal[3]
    group.IS4=playersDF.informalSignal[4]
    group.IS5=playersDF.informalSignal[5]
    group.FS1=playersDF.formalSignal[1].astype(int)
    group.FS2=playersDF.formalSignal[2].astype(int)
    group.FS3=playersDF.formalSignal[3].astype(int)
    group.FS4=playersDF.formalSignal[4].astype(int)
    group.FS5=playersDF.formalSignal[5].astype(int)
    
class Player(BasePlayer):
    informalSignal = models.FloatField(initial=0, label='Please invest in your informal signals ')
    quality = models.FloatField(initial=0, label='Please enter the quality level from 0 to 100 for your product', max=C.MAXIMUM_QUALITY)
    perceivedQuality = models.FloatField()
    Demand = models.FloatField()
    price = models.FloatField(initial=0, label='Please enter an amount as your price')
    Cost = models.FloatField(initial=0)
    profit = models.FloatField()
    qualityRank = models.FloatField()
    formalSignal = models.FloatField(initial=0, max=1)
def cost_function(player: Player):
    if(player.quality<60):
        player.formalSignal=0
    
    player.Cost=player.quality+.5*player.informalSignal+10*player.formalSignal
class Introduction(Page):
    form_model = 'player'
class Decide(Page):
    form_model = 'player'
    form_fields = ['quality', 'informalSignal', 'formalSignal']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        cost_function(player)
class Price(Page):
    form_model = 'player'
    form_fields = ['price']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
page_sequence = [Introduction, Decide, Price, ResultsWaitPage, Results]
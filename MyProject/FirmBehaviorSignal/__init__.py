
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'FirmBehaviorSignal'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 50
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
    winning_profit = models.FloatField(initial=0)
    second_profit = models.FloatField(initial=0)
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
    
    #Demand for Start at highest Quality:
    if playerRank.perceivedQuality[5]==playerRank.perceivedQuality[4]:
        if playerRank.price[5]>playerRank.price[4]:
            demand5=0
        if playerRank.perceivedQuality[5]==playerRank.perceivedQuality[3]:
            if playerRank.price[5]>playerRank.price[3]:
                demand5=0
            if playerRank.perceivedQuality[5]==playerRank.perceivedQuality[2]:
                if playerRank.price[5]>playerRank.price[2]:
                    demand5=0
                if playerRank.perceivedQuality[5]==playerRank.perceivedQuality[1]:
                    if playerRank.price[5]>playerRank.price[1]:
                        demand5=0
                    else: 
                        demand5=playerRank.price[5]/playerRank.perceivedQuality[5] - (playerRank.price[1]/playerRank.perceivedQuality[1])
                else:demand5=playerRank.price[5]/playerRank.quality[5]-(playerRank.price[5]-playerRank.price[1])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[1])    
            else:
                demand5=playerRank.price[5]/playerRank.quality[5]-(playerRank.price[5]-playerRank.price[2])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[2])
        else:
             demand5=playerRank.price[5]/playerRank.quality[5]-(playerRank.price[5]-playerRank.price[3])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[3])
    else:
        demand5=playerRank.price[5]/playerRank.quality[5]-(playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4])
    
    #Demand for 4th highest PQ:                                                                                  
    if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[5]:
        #Demand for 4th if quality is same for 5 and 4
        if playerRank.price[4]>playerRank.price[5]:
            demand4=0
        else:
            if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[3]:
                if playerRank.price[4]>playerRank.price[3]:
                    demand4=0
                if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[2]:
                    if playerRank.price[4]>playerRank.price[2]:
                        demand4=0
                    if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[1]:
                        if playerRank.price[4]>playerRank.price[1]:
                            demand4=0
                        else: 
                            demand4=playerRank.price[4]/playerRank.perceivedQuality[4] - (playerRank.price[1]/playerRank.perceivedQuality[1])
                    else:
                        demand4=playerRank.price[4]/playerRank.quality[4]-(playerRank.price[4]-playerRank.price[1])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[1])    
                else:
                    demand4=playerRank.price[4]/playerRank.quality[4]-(playerRank.price[4]-playerRank.price[2])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[2])
            else:
                 demand4=playerRank.price[4]/playerRank.quality[4]-(playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3])
    else:
        if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[3]:
                if playerRank.price[4]>playerRank.price[3]:
                    demand4=0
                if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[2]:
                    if playerRank.price[4]>playerRank.price[2]:
                        demand4=0
                    if playerRank.perceivedQuality[4]==playerRank.perceivedQuality[1]:
                        if playerRank.price[4]>playerRank.price[1]:
                            demand4=0
                        else: 
                            demand4=(playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4]) - (playerRank.price[1]/playerRank.perceivedQuality[1])
                    else:
                        demand4=(playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4])-(playerRank.price[4]-playerRank.price[1])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[1])    
                else:
                    demand4=(playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4])-(playerRank.price[4]-playerRank.price[2])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[2])
        else:
                 demand4=((playerRank.price[5]-playerRank.price[4])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[4]))-((playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3]))
    
    #Demand for 3rd highest PQ: 
    if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[4]:
        if playerRank.price[3]>playerRank.price[4]:
            demand3=0
        #Quality for 3=4, check 5 as well
        if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[5]:
            #Quality for 3rd  is same for 5 and 4
            if playerRank.price[3]>playerRank.price[5]:
                demand3=0
            else:
                if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[2]:
                    if playerRank.price[3]>playerRank.price[2]:
                        demand3=0
                    if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[1]:
                        if playerRank.price[3]>playerRank.price[1]:
                            demand3=0
    
                        else: 
                            demand3=playerRank.price[3]/playerRank.perceivedQuality[3] - (playerRank.price[1]/playerRank.perceivedQuality[1])
                    else:
                        demand3=playerRank.price[3]/playerRank.quality[3]-(playerRank.price[3]-playerRank.price[1])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[1])    
                else:
                    demand3=playerRank.price[3]/playerRank.quality[3]-(playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[2])
        else: #3 & 5 are different
            if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[2]:
                    if playerRank.price[3]>playerRank.price[2]:
                        demand3=0
                    if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[1]:
                        if playerRank.price[3]>playerRank.price[1]:
                            demand3=0
                        else:
                            demand3=(playerRank.price[5]-playerRank.price[3])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[3])-(playerRank.price[1])/(playerRank.perceivedQuality[1])    
                    else:
                        demand3=(playerRank.price[5]-playerRank.price[3])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[3])-(playerRank.price[3]-playerRank.price[1])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[1])
            else:
                     demand3=((playerRank.price[5]-playerRank.price[3])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[3]))-((playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2]))
    else:
        if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[2]:
                    if playerRank.price[3]>playerRank.price[2]:
                        demand3=0
                    if playerRank.perceivedQuality[3]==playerRank.perceivedQuality[1]:
                        if playerRank.price[3]>playerRank.price[1]:
                            demand3=0
                        else:
                            demand3=(playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3])-(playerRank.price[1])/(playerRank.perceivedQuality[1])    
                    else:
                        demand3=(playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3])-(playerRank.price[3]-playerRank.price[1])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[1])
        else:
                demand3=((playerRank.price[4]-playerRank.price[3])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[3]))-((playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2]))  
    
    #Demand for 2nd highest PQ: 
    #Check if equal to lowest:
    if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[1]:
        if playerRank.price[2]>playerRank.price[1]:
            demand2=0
    
        if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[3]:
            if playerRank.price[2]>playerRank.price[3]:
                demand2=0
    
            if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[4]:
                if playerRank.price[2]>playerRank.price[4]:
                    demand2=0
    
                if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[5]:
                    if playerRank.price[2]>playerRank.price[5]:
                        demand2=0
    
                    else:
                        demand2=playerRank.price[2]/playerRank.perceivedQuality[2]-(playerRank.price[1]/playerRank.perceivedQuality[1])
                else:
                    demand2=(playerRank.price[5]-playerRank.price[2])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[2])-(playerRank.price[1]/playerRank.perceivedQuality[1])
            else: 
                demand2=(playerRank.price[4]-playerRank.price[2])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[2])-(playerRank.price[1]/playerRank.perceivedQuality[1])
        else: 
            demand2=(playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2])-(playerRank.price[1]/playerRank.perceivedQuality[1])
    else: #2nd Highest is not equal to lowest
        if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[3]:
            if playerRank.price[2]>playerRank.price[3]:
                demand2=0
    
            if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[4]:
                if playerRank.price[2]>playerRank.price[4]:
                    demand2=0
    
                if playerRank.perceivedQuality[2]==playerRank.perceivedQuality[5]:
                    if playerRank.price[2]>playerRank.price[5]:
                        demand2=0
    
                    else:
                        demand2=playerRank.price[2]/playerRank.perceivedQuality[2]-(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[1]-playerRank.perceivedQuality[1])
                else:
                    demand2=(playerRank.price[5]-playerRank.price[2])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[2])-(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1])
            else: 
                demand2=(playerRank.price[4]-playerRank.price[2])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[2])-(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1])
        else: 
            demand2=(playerRank.price[3]-playerRank.price[2])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[2])-(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1])
    
    #Lowest:
    if playerRank.perceivedQuality[1]==playerRank.perceivedQuality[2]:
        if playerRank.price[1]>playerRank.price[2]:
            demand1=0
    
        if playerRank.perceivedQuality[1]==playerRank.perceivedQuality[3]:
            if playerRank.price[1]>playerRank.price[3]:
                demand1=0
    
            if playerRank.perceivedQuality[1]==playerRank.perceivedQuality[4]:
                if playerRank.price[1]>playerRank.price[4]:
                    demand1=0
    
                if playerRank.perceivedQuality[1]==playerRank.perceivedQuality[5]:
                    if playerRank.price[1]>playerRank.price[5]:
                        demand1=0
                    else:
                        demand1=(playerRank.price[5]/playerRank.perceivedQuality[5])-(playerRank.price[1]/playerRank.perceivedQuality[1])
                else:
                    demand1=(playerRank.price[5]-playerRank.price[1])/(playerRank.perceivedQuality[5]-playerRank.perceivedQuality[1])-(playerRank.price[1]/playerRank.perceivedQuality[1])
            else:
                demand1=(playerRank.price[4]-playerRank.price[1])/(playerRank.perceivedQuality[4]-playerRank.perceivedQuality[1])-(playerRank.price[1]/playerRank.perceivedQuality[1])
        else:
            demand1=(playerRank.price[3]-playerRank.price[1])/(playerRank.perceivedQuality[3]-playerRank.perceivedQuality[1])-(playerRank.price[1]/playerRank.perceivedQuality[1])
    else:
        demand1=(playerRank.price[2]-playerRank.price[1])/(playerRank.perceivedQuality[2]-playerRank.perceivedQuality[1])-(playerRank.price[1]/playerRank.perceivedQuality[1])
    
    
    
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
    group.FS1=playersDF.formalSignal[1]
    group.FS2=playersDF.formalSignal[2]
    group.FS3=playersDF.formalSignal[3]
    group.FS4=playersDF.formalSignal[4]
    group.FS5=playersDF.formalSignal[5]
    
    group.price1=group.price1.item()
    group.price2=group.price2.item()
    group.price3=group.price3.item()
    group.price4=group.price4.item()
    group.price5=group.price5.item()
    group.profit1=group.profit1.item()
    group.profit2=group.profit2.item()
    group.profit3=group.profit3.item()
    group.profit4=group.profit4.item()
    group.profit5=group.profit5.item()
    group.quality1=group.quality1.item()
    group.quality2=group.quality2.item()
    group.quality3=group.quality3.item()
    group.quality4=group.quality4.item()
    group.quality5=group.quality5.item()
    group.IS1=group.IS1.item()
    group.IS2=group.IS2.item()
    group.IS3=group.IS3.item()
    group.IS4=group.IS4.item()
    group.IS5=group.IS5.item()
    group.FS1=group.FS1.item()
    group.FS2=group.FS2.item()
    group.FS3=group.FS3.item()
    group.FS4=group.FS4.item()
    group.FS5=group.FS5.item()
    
    for p in players:
        p.perceivedQuality=p.perceivedQuality.item()
        p.Demand=p.Demand.item()
        p.profit=p.profit.item()
    
    
    
    winning_profit = max(playersDF.profit)
    firstPlace = [p for p in players if p.profit == winning_profit]
    second_profit=np.argpartition(np.array(playersDF.profit), -2)[-2]
    secondPlace = [p for p in players if p.profit== second_profit]
    for p in players:
        if p == firstPlace:
            p.first = 1
            p.payoff = 5
        else:
            p.first = 0
            p.payoff = 0
        if p == secondPlace:
            p.second = 1
            p.payoff = 2
        else:
            p.second = 0
    
    for p in players:
        p.first=np.float64(p.first)
        p.second=np.float64(p.second)
        p.first=p.first.item()
        p.second=p.second.item()

    group.winning_profit=winning_profit.item()
    group.second_profit=second_profit.item()

class Player(BasePlayer):
    informalSignal = models.FloatField(initial=0, label='Please invest in your informal signals ')
    quality = models.FloatField(initial=0, label='Please enter the quality level from 0 to 100 for your product', max=C.MAXIMUM_QUALITY)
    perceivedQuality = models.FloatField()
    Demand = models.FloatField()
    price = models.FloatField(initial=0, label='Please enter an amount as your price')
    Cost = models.FloatField(initial=0)
    profit = models.FloatField()
    formalSignal = models.FloatField(initial=0, max=1)
    first = models.FloatField(initial=0, max=1)
    second = models.FloatField(initial=0, max=1)
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

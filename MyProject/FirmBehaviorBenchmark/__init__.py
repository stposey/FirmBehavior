
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'FirmBehaviorBenchmark'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 5
    MAXIMUM_PRICE = cu(100)
    MAXIMUM_QUALITY = 100
    INFORMAL_SIGNAL = 100
    FORMAL_SIGNAL = 1
    INSTRUCTIONS_TEMPLATE = 'FirmBehaviorBenchmark/instructions.html'
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
    profit2 = models.FloatField()
    profit3 = models.FloatField()
    profit4 = models.FloatField()
    profit5 = models.FloatField()
    profit1 = models.FloatField()
def set_payoffs(group: Group):
    import pandas as pd
    
    qualities=[]
    prices=[]
    playerList=[]
    players = group.get_players()
    
    
    for p in players:
        qualities.append(p.quality)
        prices.append(p.price)
        playerList.append(p.id_in_group)
        p.perceivedQuality=p.quality
    
    
    PlayerDF = pd.DataFrame(data = {'playerid':playerList,'quality':qualities,'price':prices})
    PlayerDF['perceivedQuality']=PlayerDF.quality
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
    playerRank['profit']= playerRank.price*playerRank.demand-(playerRank.quality)*playerRank.demand
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
    
    group.price1=playersDF.price[1].item()
    group.price2=playersDF.price[2].item()
    group.price3=playersDF.price[3].item()
    group.price4=playersDF.price[4].item()
    group.price5=playersDF.price[5].item()
    group.profit1=playersDF.profit[1].item()
    group.profit2=playersDF.profit[2].item()
    group.profit3=playersDF.profit[3].item()
    group.profit4=playersDF.profit[4].item()
    group.profit5=playersDF.profit[5].item()
    group.quality1=playersDF.quality[1].item()
    group.quality2=playersDF.quality[2].item()
    group.quality3=playersDF.quality[3].item()
    group.quality4=playersDF.quality[4].item()
    group.quality5=playersDF.quality[5].item()
    
    
class Player(BasePlayer):
    quality = models.FloatField(initial=0, label='Please enter the quality level from 0 to 100 for your product', max=C.MAXIMUM_QUALITY)
    profit = models.FloatField()
    perceivedQuality = models.FloatField()
    Demand = models.FloatField(initial=0)
    price = models.FloatField(initial=0, label='Please enter an amount as your price')
    Cost = models.FloatField(initial=0)
def cost_function(player: Player):
    player.Cost=player.quality
class Introduction(Page):
    form_model = 'player'
class Decide(Page):
    form_model = 'player'
    form_fields = ['quality']
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

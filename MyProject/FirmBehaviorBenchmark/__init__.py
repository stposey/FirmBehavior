
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'FirmBehaviorBenchmark'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 10
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
    winning_profit = models.FloatField()
    second_profit = models.FloatField()
def set_payoffs(group: Group):
    import pandas as pd
    import numpy as np
    
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
    
    for p in players:
        p.Demand=p.Demand.item()
        p.profit=p.profit.item()
    
group.winning_profit = max([p.profit for p in players])
firstPlace = [p for p in players if p.price == group.winning_profit]
group.second_profit=np.argpartition([p.profit for p in players], -2)[-2]
secondPlace = [p for p in players if p.price== group.second_profit]
group.winning_proft=np.float64(group.winning_profit)
group.second_profit=np.float64(group.second_profit)
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
    for p in players:
        p.first=np.float(p.first)
        p.second=np.float(p.second)
        p.first=p.first.item()
        p.second=p.second.item()
    group.winning_profit = group.winning_profit.item()
    group.second_profit = group.second_profit.item()
class Player(BasePlayer):
    quality = models.FloatField(initial=0, label='Please enter the quality level from 0 to 100 for your product', max=C.MAXIMUM_QUALITY)
    profit = models.FloatField()
    perceivedQuality = models.FloatField()
    Demand = models.FloatField(initial=0)
    price = models.FloatField(initial=0, label='Please enter an amount as your price')
    Cost = models.FloatField(initial=0)
    first = models.FloatField(initial=0, max=1)
    second = models.FloatField(initial=0, max=1)
def cost_function(player: Player):
    player.Cost=player.quality
class PIntroduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number<4:
            return True
class PDecide(Page):
    form_model = 'player'
    form_fields = ['quality']
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number<4:
            return True
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        cost_function(player)
class PPrice(Page):
    form_model = 'player'
    form_fields = ['price']
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number<4:
            return True
class PResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number<4:
            return True
class PResults(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number<4:
            return True
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number>3:
            return True
class Decide(Page):
    form_model = 'player'
    form_fields = ['quality']
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number>3:
            return True
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        cost_function(player)
class Price(Page):
    form_model = 'player'
    form_fields = ['price']
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number>3:
            return True
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
page_sequence = [PIntroduction, PDecide, PPrice, PResultsWaitPage, PResults, Introduction, Decide, Price, ResultsWaitPage, Results]

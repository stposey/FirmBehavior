
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'FirmBehaviorSearchSignal'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 10
    MAXIMUM_PRICE = cu(100)
    MAXIMUM_QUALITY = 100
    INFORMAL_SIGNAL = 100
    FORMAL_SIGNAL = 1
    INSTRUCTIONS_TEMPLATE = 'FirmBehaviorSearchSignal/instructions.html'
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
    
    
    firms=[1,2,3,4,5]
    repeat = np.repeat(np.arange(1,6), 200).reshape(200,-1)
    for i in range(200):
        np.random.shuffle(firms)
        repeat[i,:]=firms
    firm1=repeat[:,0]
    firm2=repeat[:,1]
    firm3=repeat[:,2]
    firm4=repeat[:,3]
    firm5=repeat[:,4]
    theta=np.random.randint(1, 100, 200)
    priceC=np.random.randint(1, 100, 200)
    buy=[0 for element in range(200)]
    priceQualityC=np.divide(priceC,theta)
    customers=pd.DataFrame(data= {'theta':theta,'firm1':firm1,'firm2':firm2,'firm3':firm3,'firm4':firm4,'firm5':firm5,'price':priceC,'priceQuality':priceQualityC})
    
    qualities=[]
    prices=[]
    playerList=[]
    informalSignals=[]
    formalSignals=[]
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
    playerDF = pd.DataFrame(data = {'playerid':playerList,'quality':qualities,'price':prices, 'informalSignals':informalSignals, 'formalSignals':formalSignals})
    playerDF['perceivedQuality']=playerDF.quality+np.log(playerDF.informalSignals)+10*playerDF.formalSignals
    playerDF['priceQuality']=np.divide(playerDF.price,playerDF.perceivedQuality)
    playerDF = playerDF.sort_values(by = ['playerid'])
    
    for i in range(200):
        choice1=customers.firm1[i]-1
        choice2=customers.firm2[i]-1
        choice3=customers.firm3[i]-1
        choice4=customers.firm4[i]-1
        choice5=customers.firm5[i]-1
        pqC=customers.priceQuality[i]
        minPQ=playerDF.priceQuality[choice1]
        minFirm=choice1+1
        if pqC>playerDF.priceQuality[choice1]:  #choice 1 IF consumer has higher pq ratio they choose choice 1. If not, they move on with search
            buy[i]=minFirm
            continue
        else: 
            pqC=pqC*1.5 #search cost is not flat
        if playerDF.priceQuality[choice2]<playerDF.priceQuality[choice1]:
            minPQ=playerDF.priceQuality[choice2]
            minFirm=choice2+1
        if pqC>playerDF.priceQuality[choice2]: #choice 2. If consumer has higher pq ratio they choose choice 2. If not they move on with search
            buy[i]=minFirm
            continue
        else:
            pqC=pqC*1.5 
    
    
        if playerDF.priceQuality[choice3]<minPQ:
            minPQ=playerDF.priceQuality[choice3]
            minFirm=choice3+1
        if pqC>playerDF.priceQuality[choice3]: #Choice3
            buy[i]=minFirm
            continue
        else:
            pqC=pqC*1.5
    
    
        if playerDF.priceQuality[choice4]<minPQ:
            minPQ=playerDF.priceQuality[choice4]
            minFirm=choice4+1
        if pqC>playerDF.priceQuality[choice4]: #Choice4
            buy[i]=minFirm
            continue
        else:
            pqC=pqC*1.5
    
        if playerDF.priceQuality[choice5]<minPQ:
            minPQ=playerDF.priceQuality[choice5]
            minFirm=choice5+1
        if pqC>playerDF.priceQuality[choice5]: #Choice5
            buy[i]=minFirm
            continue
        else:
            buy[i]=0 #Consumer opts out from buying
    
    customers['buy']=buy
    demand=[buy.count(1),buy.count(2),buy.count(3),buy.count(4),buy.count(5)]
    playerDF['demand']=np.float64(demand)
    playerDF['profit']=playerDF.price*playerDF.demand-(playerDF.quality-.5*playerDF.informalSignals-playerDF.formalSignals*10)*playerDF.demand
    
    
    for p in players:
        if p.id_in_group==1:
            p.Demand=playerDF.demand[0]
        if p.id_in_group==2:
            p.Demand=playerDF.demand[1]
        if p.id_in_group==3:
            p.Demand=playerDF.demand[2]
        if p.id_in_group==4:
            p.Demand=playerDF.demand[3]
        if p.id_in_group==5:
            p.Demand=playerDF.demand[4]   
    
    for p in players:
        p.profit=(p.price-p.Cost)*p.Demand
    
    group.price1=round(playerDF.price[0],2)
    group.price2=round(playerDF.price[1],2)
    group.price3=round(playerDF.price[2],2)
    group.price4=round(playerDF.price[3],2)
    group.price5=round(playerDF.price[4],2)
    group.profit1=round(playerDF.profit[0],2)
    group.profit2=round(playerDF.profit[1],2)
    group.profit3=round(playerDF.profit[2],2)
    group.profit4=round(playerDF.profit[3],2)
    group.profit5=round(playerDF.profit[4],2)
    group.quality1=playerDF.quality[0]
    group.quality2=playerDF.quality[1]
    group.quality3=playerDF.quality[2]
    group.quality4=playerDF.quality[3]
    group.quality5=playerDF.quality[4]
    group.IS1=playerDF.informalSignals[0]
    group.IS2=playerDF.informalSignals[1]
    group.IS3=playerDF.informalSignals[2]
    group.IS4=playerDF.informalSignals[3]
    group.IS5=playerDF.informalSignals[4]
    group.FS1=playerDF.formalSignals[0]
    group.FS2=playerDF.formalSignals[1]
    group.FS3=playerDF.formalSignals[2]
    group.FS4=playerDF.formalSignals[3]
    group.FS5=playerDF.formalSignals[4]
    
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
        p.Demand=p.Demand.item()
        p.profit=p.profit.item()
    
    
def Winner(group: Group):
    last_7_rounds = range(3, 11)
    players = group.get_players()
    for n in players:
        n.total_profit = sum(p.profit for p in n.in_all_rounds() if p.round_number in last_7_rounds)
    
    winner=max(p.total_profit for p in players)
    for p in players:
        if winner==p.total_profit:
            p.first=1
            p.payoff=5
class Player(BasePlayer):
    informalSignal = models.FloatField(initial=0, label='Please invest in your informal signals ')
    quality = models.FloatField(initial=0, label='Please enter the quality level from 0 to 100 for your product', max=C.MAXIMUM_QUALITY)
    profit = models.FloatField()
    Demand = models.FloatField(initial=0)
    price = models.FloatField(initial=0, label='Please enter an amount as your price')
    formalSignal = models.FloatField(blank=True, initial=0, label='Choose whether to apply or not apply formal signals ', max=1, min=0)
    Cost = models.FloatField(initial=0)
    first = models.FloatField(initial=0, max=1)
    total_profit = models.FloatField(initial=0)
def cost_function(player: Player):
    player.Cost=player.quality+.5*player.informalSignal+10*player.formalSignal
class Introduction(Page):
    form_model = 'player'
class Decide(Page):
    form_model = 'player'
    form_fields = ['informalSignal', 'quality', 'formalSignal']
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
class FinalWaitPage(WaitPage):
    after_all_players_arrive = Winner
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number==C.NUM_ROUNDS:
            return True
class Final(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        if subsession.round_number==C.NUM_ROUNDS:
            return True
page_sequence = [Introduction, Decide, Price, ResultsWaitPage, Results, FinalWaitPage, Final]
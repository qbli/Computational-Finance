from random import gauss, seed
import numpy as np

#define the constant
NOM=100000
K0=1
CP_set1=0.015
CP_set2=0.0115
KI=0.92
AC=1
sigma=0.289
T=0.25
N=90
S = 6.27
r = 0.0075
delta_t=T/N

def monte_carlo_simulation3(I,CP):
    payoff=[]
    K = S * K0 #strike price
    Pc = S * AC #auto-call price
    Pk = S * KI #knock-in price
    for i in range(I):
        flag_knock=False #knock in check
        flag_early_ter=False #early termination check
        path1 = []
        first_coupon = NOM * CP / pow((1 + r), 0.0833)
        second_coupon = NOM * CP / pow((1 + r), 0.1666)
        third_coupon=NOM * CP / pow((1 + r), 0.25)
        for t in range(N + 1):

            if t == 0:
                path1.append(S)
            else:
                z = gauss(0.0, 1.0)
                Delta_S = r * path1[t - 1] * delta_t + sigma * path1[t - 1] * z * np.sqrt(delta_t)
                S_T = path1[t - 1] + Delta_S# the t time stock price
                path1.append(S_T)

                # #check knock-in event
                while not flag_knock and not flag_early_ter:
                    if S_T < Pk:
                        flag_knock=True
                    elif t>30 and S_T>=Pc:
                        flag_early_ter = True
                    break

                #two conditions: early termination and on the expiry day
                if 30 < t < 60 and S_T >= Pc:
                    early_ter_recieve=NOM+NOM*CP*(t-30)/30
                    early_ter_payoff = early_ter_recieve/pow((1+r),t/30*0.0833)-NOM
                    total_payoff=first_coupon+early_ter_payoff
                    payoff.append(total_payoff)
                    break;

                if 60<=t<90 and S_T >= Pc:
                    early_ter_recieve = NOM + NOM * CP * (t - 60) / 30
                    early_ter_payoff=early_ter_recieve/pow((1+r),t/60*0.1666)-NOM
                    total_payoff=first_coupon+second_coupon+early_ter_payoff
                    payoff.append(total_payoff)
                    break;

                #on the expiry day
                if t==N-1 and not flag_knock:
                    total_payoff=NOM/pow((1+r),0.25)-NOM
                    payoff.append(total_payoff)
                elif flag_knock and t==N-1 and S_T>=K:
                    total_payoff=first_coupon+second_coupon+third_coupon+NOM/pow((1+r),0.25)-NOM
                    payoff.append(total_payoff)
                elif t==N-1 and flag_knock and S_T<K:
                    total_payoff=first_coupon+second_coupon+third_coupon+(NOM*S_T/K)/pow((1+r),0.25)-NOM
                    payoff.append(total_payoff)

    return np.mean(payoff)

if __name__ == "__main__":
    I_item = [1000, 10000, 100000, 500000]
    test_i = 100
    all_fair_price = []

    for i in I_item:
        #calculate the question 1
        fair_price = monte_carlo_simulation3(i, CP_set1)
        all_fair_price.append(fair_price)
        print('the fair value of simulate', i, 'times is :', fair_price)
        print('the profit of bank in each case in', i, 'times simalation', 'is', -fair_price + S)

        # calculate the question2
        fair_price2 = monte_carlo_simulation3( i, CP_set2)
        print('the fair value of simulate', i, 'times in cp set 2 is :', fair_price2)
        print("the additional profit is :", -fair_price2 + fair_price)

    #calculate the question3

    CP_item=np.arange(0.005,0.01,.0001)
    profit=[]
    margin=[]
    for i in CP_item:
        fair_price3=monte_carlo_simulation3(500000,i)
    # print(-fair_price3/NOM)
        margin.append(-fair_price3/NOM)
        profit_margin=abs(-fair_price3/NOM)
        gap=abs(profit_margin-0.023)
        profit.append(gap)


    print('test')
    print('the cp =',np.argmin(profit)/10000+0.005)
    print('the gap is :',np.min(profit))

    #test module
    # fair_price3 = monte_carlo_simulation3(1000, test_cp)
    # profit_margin = -fair_price3 / NOM
    # print(profit_margin)












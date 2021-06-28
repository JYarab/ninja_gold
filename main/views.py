from django.shortcuts import render, redirect
import random
from time import localtime, strftime


def index(request):
    return render(request, 'index.html')

def set_win(request):
    request.session['win_gold'] = request.POST['win_gold']
    request.session['win_adv'] = request.POST['win_adv']

    # print(f'win gold ={request.session["win_gold"]} win adv = {request.session["win_adv"]}')
    return redirect('/')

def farm(request):
    request.session['location'] = 'farm'
    return redirect('/process_money')

def cave(request):
    request.session['location'] = 'cave'
    return redirect('/process_money')

def house(request):
    request.session['location'] = 'house'
    return redirect('/process_money')

def casino(request):
    request.session['location'] = 'casino'
    return redirect('/process_money')

def process_money(request):
#populate session data if none exists
    win_gold = request.session.get('win_gold')
    if win_gold is '' or win_gold is None:
        win_gold = 0
    request.session['win_gold'] = win_gold

    win_adv = request.session.get('win_adv')
    if win_adv is '' or win_adv is None:
        win_adv = 0
    request.session['win_adv'] = win_adv

    gold = request.session.get('gold')
    if gold is None:
        gold = 0
    request.session['gold'] = gold
    
    adventures = request.session.get('adventures')
    if adventures is None:
        adventures = 0
    request.session['adventures'] = adventures

    history = request.session.get('history')
    if history is None:
        history = []
    request.session['history'] = history

    #check for valid win conditions
    if(int(request.session['win_gold']) == 0 or int(request.session['win_adv']) == 0):
        request.session['history'].append(f'Enter valid win conditions to play, reset and again. {strftime("%Y-%m-%d %H:%M %p",localtime())}')

    #complete an adventure
    elif(int(request.session['adventures']) < int(request.session['win_adv']) and int(request.session['gold']) < int(request.session['win_gold'])):
        
        request.session['adventures'] += 1

        #Farm Selected
        if(request.session['location'] == 'farm'):
            gold_earned = random.randint(10,20)
            request.session['gold'] += gold_earned
            log_adv(request, gold_earned)
            win_check(request)

        # Cave Selected 
        if(request.session['location'] == 'cave'):
            gold_earned = random.randint(5,10)
            request.session['gold'] += gold_earned
            log_adv(request, gold_earned)
            win_check(request)

        
        #House Selected
        if(request.session['location'] == 'house'):
            gold_earned = random.randint(2,5)
            request.session['gold'] += gold_earned
            log_adv(request, gold_earned)
            win_check(request)

        #Casino selected 
        if(request.session['location'] == 'casino'):
            gold_earned = random.randint(-50,50)
            request.session['gold'] += gold_earned
            if (gold_earned > 0):
                log_adv(request, gold_earned)
                win_check(request)
            else:
                request.session['history'].append(f'Adventure number {request.session["adventures"]}. Oh No!! {abs(gold_earned)} gold lost at the {request.session["location"]}! {strftime("%Y-%m-%d %H:%M %p",localtime())}')
                win_check(request)
    return redirect('/')

def reset(request):
    request.session.flush()
    print("clear session")
    return redirect('/')

def log_adv(request, gold_earned):
    request.session['history'].append(f'Adventure number {request.session["adventures"]}. Earned {gold_earned} gold from the {request.session["location"]}! {strftime("%Y-%m-%d %H:%M %p",localtime())}')

def win_check(request):
    if (int(request.session['adventures']) <= int(request.session['win_adv']) and int(request.session['gold']) >= int(request.session['win_gold'])):
        request.session['history'].append(f'Congradulations you won, reset to play again. {strftime("%Y-%m-%d %H:%M %p",localtime())}')
    elif (int(request.session['adventures']) >= int(request.session['win_adv']) and int(request.session['gold']) < int(request.session['win_gold'])):
        request.session['history'].append(f'Adventure over,  not enough gold, reset to try again. {strftime("%Y-%m-%d %H:%M %p",localtime())}')

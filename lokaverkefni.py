# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:55:31 2022

@author: OttoIvars
"""

import numpy as np
import os

#allowed_final_path = (os.path.join(os.getcwd(), "allowed_words.txt"))
#print(allowed_final_path)
allowed_final = np.loadtxt(os.path.join(os.getcwd(), "allowed_words.txt"),dtype='str')
possible_final = np.loadtxt(os.path.join(os.getcwd(), "possible_words.txt"),dtype='str')
#allowed_final = np.loadtxt("C:/Users/ottom/Documents/Mynsto/allowed_words.txt" , dtype='str')
#possible_final = np.loadtxt("C:/Users/ottom/Documents/Mynsto/possible_words.txt" , dtype='str') 

n_allow = 12953
n_possible = 2309

allowed_final_char = list(allowed_final)
possible_final_char = list(possible_final)

##
def charToInt(lst): 
  t = []
  for i in range(len(lst)):
    for j in range(5):
      t.append(ord(lst[i][j]))  
  m = np.array(t).reshape(len(lst),5)  
  return m

##
def stringToInt(s):
  t = []
  for j in range(5):
    t.append(ord(s[j]))
  m = np.array(t).reshape(1,5)
  return m

##
ascii_const = ord('a')

##
def scorePool(pool):
  ascii_const = ord('a')
  fjoldi = np.zeros((26,5),dtype = 'int')
  for i in range(len(pool)):
   for j in range(5):
      ascii = ord(pool[i][j])
      fjoldi[ascii-ascii_const, j] += 1
  scoreBoard = []
  likindi = fjoldi.astype(np.float64)/n_possible

  for i in range(len(pool)):
    score = 0.0
    for j in range(5):
      score += likindi[ord(pool[i][j])-ascii_const,j]
    scoreBoard.append(score)
  return scoreBoard

##
def bestWord(pool):
  scores = scorePool(pool)
  index = np.argmax(scores)
  word = pool[index]
  return word



##
def green(pool,guess,svar):
  b1 = False
  for i in range(5):
    if svar[i] == 2:
      break
    if i == 4:
      b1 = True

  if b1: 
    return pool

  lst = []
  m = charToInt(pool)
  for i in range(len(pool)):
    veraMed = False
    for j in range(5):
      if svar[j] == 2:
        if m[i,j] != guess[0][j]:
         break
      if j == 4:
        veraMed = True

    if veraMed:
         lst.append(pool[i])

    
  pool2 = lst
  return pool2

##
def yellow(pool2, svar, guess):
  m = charToInt(pool2)
  b1 = False
  for i in range(5):
    if svar[i] == 1:
      break
    if i == 4:
      b1 = True

  if b1: 
    return pool2
    
  lst = []
  for i in range(len(pool2)):
    b2 = False
    b3 = False
    for j in range(5):
      if svar[j] == 1:
        for k in range(5):
             if svar[k] != 2:
               if (j != k):
                if(m[i,k] == guess[0][j]) and (m[i,j] != guess[0][j]):
                  break
             if k == 4:
                b2 = True
      if b2:
        break
        
      if j == 4:
       b3 = True    

    if b2 == False:
      if b3 == True:
        lst.append(pool2[i])

  return lst

##
def grey(pool3, svar, guess, komid_char):
  m = charToInt(pool3)
  b1 = False
  for i in range(5):
    if svar[i] == 0:
      break
    if i == 4:
      b1 = True

  if b1: 
    return pool3


  lst = []
  m = charToInt(pool3)
  for i in range(len(pool3)):
    takaUt = False
    for j in range(5):
      if svar[j] == 0:
        for k in range(5):
          if svar[k] != 2:
            if (guess[0][j] == m[i,k]) and (chr(guess[0][j]) not in komid_char):
              takaUt = True;
              break
        if takaUt:
          break
    if takaUt == False:
      lst.append(pool3[i])  
  pool4 = lst
  return pool4

##

##
def giska(guess, target, pool):
  komid_char = []
  del komid_char
  #Tékkum hvort stafur sé endurtekinn

  svar = [0, 0, 0, 0, 0]
  for i in range(5):
    if guess[0][i] == target[0][i]:
      svar[i] = 2     #Ef stafur er á réttum stað setja grænan lit í giski

  pool2 = green(pool,guess,svar) #Tökum út öll orð sem eru ekki með græna staf á réttum stað

  komid_gisk = []  #"strokum stafi"
  komid_target =[] #Þurfum að ha
  komid_char = []
  for i in range(5):  #Ítrum yfir svar og gisk til að finna gulu stafina
    if svar[i] == 0:
      for j in range(5):  #Ítrum yfir target
        if svar[j] != 2:
          if j != i:
            if guess[0][i] == target[0][j]:
              if (i not in komid_gisk) and (j not in komid_target):    #Svo við fáum ekki 2 gula stafi ef það ætti að vera 1
                svar[i] = 1
                komid_gisk.append(i)
                komid_char.append(chr(guess[0][i]))
                komid_target.append(j)

  pool3 = yellow(pool2, svar, guess) #Tökum út öll orð sem eru ekki með gulan staf
  pool4 = grey(pool3, svar, guess, komid_char)   #Tökum út öll orð sem innihalda gráan staf

  return pool4, svar


def prentalitur(guessWord, svar): #,end = ''
    for i in range(5):
        if svar[i] == 2:
            print('\033[1;32m' + guessWord[i] + '\033[1;37m',end = '')
        elif svar[i] == 1:
            print('\033[1;33m' + guessWord[i] + '\033[1;37m',end = '')
        else:        
            print('\033[1;31m' + guessWord[i] + '\033[1;37m',end = '')
    #print()


print('Skrifaðu \'bot\' ef þú vilt gefa bot-inum orð til að leysa sjálfur')
print('Skrifaðu \'hjalp\' ef þú vilt fá hjálp með Wordle dagsins')
hvadaleik = input()

if hvadaleik == 'bot':
    ##I/O hluti
    #Hermun með besta orði
    #b = input('skrifaðu eihv:'
    sum = 0
    print('possible_words.txt:')
    print(*possible_final)
    targetWord = input('Skrifaðu orð sem er í possible_words.txt:')#random.choice(possible_final_char)
    target = stringToInt(targetWord)
    pool = possible_final_char
    guessWord = bestWord(possible_final_char)
    print()
    print(targetWord)
    print()
    guess1 = stringToInt(guessWord)
    words, svar = giska(guess1, target, pool)
    print('Veljum orðið ',end = '')
    prentalitur(guessWord,svar)
    print(' úr ' + str(len(pool))+  ' mögulegum giskum')
    #print(svar)
    
    if svar == [2, 2, 2, 2, 2]:
      sum = sum + 1
      
    else:
        for j in range(5):
          guessWord = bestWord(words)
          guess = stringToInt(guessWord)
          words_old = words
          words, svar = giska(guess, target, words)
          print('Veljum orðið ',end = '')
          prentalitur(guessWord,svar)
          print(' úr ' + str(len(words_old))+  ' mögulegum giskum')
          if svar == [2,2,2,2,2]:
            sum = sum+2+j
            break
    
      
    print('Leyst með ' + str(sum) + ' giskum')

elif hvadaleik == 'hjalp':
    print()
    print('Hjálp með Wordle dagsins!')
    print('Skrifaðu inn orðið sem þú settir inn á Wordle síðunni á eftir orð:')
    print('Skrifaðu litina á sérhverjum staf,' ,end='')
    print('\033[1;32m' +' 2 fyrir grænan' + '\033[1;37m' +', ' ,end='')
    print('\033[1;33m' + '1 fyrir gulan' + '\033[1;37m')
    print('og 0 fyrir gráan/' + '\033[1;31m'+'rauðan.' +'\033[1;37m' +' á eftir')
    print('\n'+ 'Dæmi')
    print('orð: ', end='')
    prentalitur('slate', [0,2,2,0,1])
    print()
    print('litir: 02201')
    ##hjálp hluti
    #Hermun með besta orði
    #
    print('\n'+'Hint: gott upphafsgisk er t.d. \'slate\' ')
    print('\n' + 'Ef þú vilt hætta, ekki skrifa neitt á eftir \'orð:\' og ýttu á Enter.')
    pool = possible_final_char
    sum = 0
    while(True):
        sum = sum + 1
        ord_in = input('orð:')
        if len(ord_in) == 0:
            break
        litir_in = input('litir:')
        litir_in_char = list(litir_in)
        litir_in_int = []
        for i in range(5):
            litir_in_int.append(int(litir_in_char[i]))
        #print(litir_in_int)

        
        #guessWord = bestWord(words)
        #guess = stringToInt(guessWord)
        #words_old = words
        #words, svar = giska(guess, target, words)
        pool = green(pool,stringToInt(ord_in) , litir_in_int)
        pool = yellow(pool, litir_in_int, stringToInt(ord_in))
        pool = grey(pool, litir_in_int, stringToInt(ord_in), [])
        print('Veljum orðið ',end = '')
        print('\033[1;32m' + bestWord(pool) + '\033[1;37m',end = '')
        print(' úr ' + str(len(pool))+  ' mögulegum giskum')
        if litir_in_int == [2,2,2,2,2]:
          print()
          print('Til hamingju þú vannst með ' + str(sum) + ' giskum!')
          break
else:
    print('\033[1;31m'+'Invalid input, U donut' + '\033[1;37m')
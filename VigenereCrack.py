'''
Created on May 9, 2012

@author: Pasieka Manuel , mapa17@posgrado.upv.es
'''

import sys
import os
import subprocess
import math


#Spanish letter frequency distribution
#source : http://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras
#Alternative: #source : http://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras
slf = {}
slf["A"] = 12.53
slf["B"] = 1.42
slf["C"] = 4.68
slf["D"] = 5.96
slf["E"] = 13.68
slf["F"] = 0.69
slf["G"] = 1.01
slf["H"] = 0.70
slf["I"] = 6.25
slf["J"] = 0.44
slf["K"] = 0.01
slf["L"] = 4.97
slf["M"] = 3.15
slf["N"] = 6.71
slf["Ñ"] = 0.31
slf["O"] = 8.68
slf["P"] = 2.51
slf["Q"] = 0.88
slf["R"] = 6.87
slf["S"] = 7.98
slf["T"] = 4.63
slf["U"] = 3.93
slf["V"] = 0.90
slf["W"] = 0.02
slf["X"] = 0.22
slf["Y"] = 0.90
slf["Z"] = 0.52

#Scale to percent
for l in slf:
    slf[l] = slf[l] * 0.01
    
#Defines the order of letters!
spanishAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ','O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
spanishX = 0
for l in spanishAlphabet:
    spanishX += slf[l]**2    

#Englisch letter frequency distribution
#Source http://en.wikipedia.org/wiki/Letter_frequency

elf = {}
elf["A"] = 8.167
elf["B"] = 1.492
elf["C"] = 2.782
elf["D"] = 4.253
elf["E"] = 12.702
elf["F"] = 2.228
elf["G"] = 2.015
elf["H"] = 6.094
elf["I"] = 6.966
elf["J"] = 0.153
elf["K"] = 0.772
elf["L"] = 4.025
elf["M"] = 2.406
elf["N"] = 6.749
elf["O"] = 7.50
elf["P"] = 1.929
elf["Q"] = 0.095
elf["R"] = 5.987
elf["S"] = 6.327
elf["T"] = 9.056
elf["U"] = 2.758
elf["V"] = 0.978
elf["W"] = 2.360
elf["X"] = 0.15
elf["Y"] = 1.974
elf["Z"] = 0.074

#Scale to percent
for l in elf:
    elf[l] = elf[l] * 0.01
    
#Defines the order of letters!
englischAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
englischX = 0
for l in englischAlphabet:
    englischX += elf[l]**2    


def frequencyCorrelation(text, letterFrequencyDistribution, debug=False):
    s = text
    lfd = letterFrequencyDistribution
    
    #Create letterFrequencyTable for text
    lf = {}
    n = len(s)
    sum = 0
    for i in lfd.keys():
        lf[i] = float(s.count(i) / n)
        sum += lf[i]
    
    if debug : print("Letter frequency distribution for text , sum {} , length {} distribution {}".format(sum,n,lf))
    
    #Calculate the correlation
    x = 0.0
    for i in lfd.keys():
        x +=  lfd[i] * lf[i]

    if debug : print("Calculated correlation is {}".format(x))
    return x

def alignInColums(text, nColums):
    t = []
    for i in range(0,nColums):
        t.append("")
    i = 0
    for c in text:
        t[i%nColums]+=c
        i+=1
    return t

def joinColums(columTable):
    nColums = len(columTable)
    s = ""
    itCnt = 0
    while True:
        for i in range(0, nColums):
            try:
                s += columTable[i][itCnt]
            except IndexError:
                return s;
        itCnt += 1

def caeserCipher(text, letter, alphabet):
    a = alphabet
    al = len(a)
    li = {} #LetterIndex , hash with each letter and its position int he alphabet
    for l in a:
        li[l] = a.index(l)
    shift = li[letter]
    if(shift < 0):
        raise ValueError #Letter is not part of the alphabet
    s = ""
    for c in text:
        cp = li[c]
        if(cp < 0):
            raise IndexError #Letter is not part of the alphabet        
        s += a[ (cp+shift)%al ]
    return s

def caeserDecipher(text,letter,alphabet):
    al = len(alphabet)
    lp = alphabet.index(letter)
    if(lp < 0):
        raise ValueError
    lp = (al - lp)%al
    return caeserCipher(text, alphabet[lp], alphabet)

def getPasswords(columTable, keyLength, letterFrequencyDistribution, alphabet, languageX, debug=False):
    lfd = letterFrequencyDistribution
    cT = columTable
    kL = keyLength
    #Will hold the xs for each ceaserShift
    xs = []
    for i in range(0,kL):
        xs.append([])
    
    if debug : print("Calculating difference of letter distribution for each column and shift")
    for l in alphabet:
        i = 0
        for c in cT:
            c2 = caeserDecipher(c, l, alphabet)
            x = frequencyCorrelation(c2, lfd)
            x = math.sqrt((languageX-x)**2) * 100.0 #Highlight the difference to Spanish X
            xs[i].append(x)            
            i+=1
    
    xMin = 0
    pLikely = ""
    #Get the two most probable letters for each column
    if debug : print("\nTwo Most probable key letter are")
    kLikly = []
    for y in xs:
        x = list(y)
        m1 = min(x)
        i1 = x.index(m1)
        l1 = alphabet[i1] 
        x[i1] = 100.0
        m2 = min(x)
        i2 = x.index(m2)
        l2 = alphabet[i2]
        kLikly.append( (l1,l2,m1,m2) )
        
        pLikely += l1
        xMin += m1
        
    print("\nDistance of the letter distribution frequency to Spanish. (lower values are better , lowest are marked with *)\n")
    
    sys.stdout.write("Column")
    for i in range(0,kL):
        sys.stdout.write("  {:02}    ".format(i))
        
    for i in range(0,len(alphabet)):
        sys.stdout.write("\n[{}]: ".format(alphabet[i]))
        for j in range(0,kL):
            if(xs[j][i] in kLikly[j]):
                sys.stdout.write("*{0:.3f}* ".format(xs[j][i]))
            else:
                sys.stdout.write("[{0:.3f}] ".format(xs[j][i]))
        sys.stdout.write("[{}]: ".format(alphabet[i]))
    
    sys.stdout.write("\nColumn")
    for i in range(0,kL):
        sys.stdout.write("  {:02}    ".format(i))
    
    
    s = joinColums(cT)
    c2 = VigenereDecipher(s, pLikely, alphabet)
    xClearText = frequencyCorrelation(c2, slf)
    
    print("\n\nMost likely password is: {} xTotal {:.3f} , xClearText {:.3f}".format(pLikely, xMin, xClearText))
    
    return (pLikely,kLikly)    

import operator

def buildPasswordList(mostLiklyKeys, maxNPasswords, debug=False):
    k = mostLiklyKeys
    kL = len(k)
    #Build password list
    pswd = []
    rating = []
    for i in range(0,kL):
        rating.append((i, k[i][3]-k[i][2]))
        
    rating.sort(key=operator.itemgetter(1))
    order = []
    for i in rating:
        order.append(i[0])
    
    if debug : print("\nKey Order list {}".format(order))
    
    #Add most likely password
    s = ""
    for i in range(0, kL):
        s += k[i][0]
    pswd.append(s)
    
    while(True):
        for i in range(1, kL+1):            
            for j in range(0,kL+1):
                s = ""
                for l in range(0,kL):
                    if(l in order[j:j+i]):
                        s+=k[l][1]
                    else:
                        s+=k[l][0]
                pswd.append(s)
                if( len(pswd) > maxNPasswords ):
                    return pswd 

def VignereCipher(text, password, alphabet):
    pl = len(password)
    a = alphabet
    al = len(a)
    li = {} #LetterIndex , hash with each letter and its position int he alphabet
    for l in a:
        li[l] = a.index(l)
        
    pShift = []
    for l in password:
        pShift.append( li[l] )
    
    s = ""
    cnt = 0
    for c in text:
        cp = li[c]
        if(cp < 0):
            raise IndexError #Letter is not part of the alphabet
        shift = pShift[cnt%pl]
        s += a[ (cp+shift)%al ]
        cnt+=1
    return s


def VigenereDecipher(text, password, alphabet):
    al = len(alphabet)
    pShift = []
    for l in password:
        pShift.append( alphabet.index(l) )
    pRevPasswd = ""
    for l in pShift:
        pRevPasswd+=( alphabet[(al - l)%al] )
    return VignereCipher(text, pRevPasswd, alphabet)

def VigenereDecipherPWList(text, alphabet, passwordList, outputPath):
    pL = passwordList
    tl = len(text)
    
    #Calculate max #chars per file
    nl = 56
    nC = 75 
    for p in pL:
        #Decrypt text with every password and write result to a text file
        s = VigenereDecipher(text, p, alphabet)
        x = frequencyCorrelation(s, slf)
        file = open(os.path.join(outputPath,"{:03}_{}.txt".format(pL.index(p),p)),"w")
        file.write("Password [{}] {}/{} Sum[(x-n)**2] = {}\n".format(p,pL.index(p),len(pL),x))
        for i in range(0,nl):
            if(i*nC > tl):
                break;
            file.write("{}\n".format(s[i*nC:(i+1)*nC]))
        file.close()

def generatePdf(cipherDir,outputPdf):
    cmd = "convert -font FreeMono-Medium {} {}".format(os.path.join(cipherDir,"*.txt"), outputPdf)                                                      
    subprocess.getstatusoutput(cmd)

def usage():
    return "{} CipherFile KeyLength/Key [OutPutPdf]".format(sys.argv[0])

def main():
   
    #Specify the letter frequency distribution and alphabet to use
    alphabet = spanishAlphabet
    letterFrequencyDistribution = slf
    languageX = spanishX
   
    #alphabet = englischAlphabet
    #letterFrequencyDistribution = elf
    #languageX = englischX
   
    if( len(sys.argv) == 3):
        print("Create letter distribution table only!")
        createLetterDistributionTableOnly = True
    else:
        createLetterDistributionTableOnly = False
        
        if( len(sys.argv) < 4):
            print("Error in Arguments!\nUsage {}".format(usage()))
            sys.exit(1)
    
    
    if( sys.argv[2].isdigit() ):
        decryptSingleFile = False
    else:
        decryptSingleFile = True
    
    cipherFile = str(sys.argv[1])
    os.path.abspath(cipherFile);
    if( os.path.isfile(cipherFile) == False ):
        print("Error! {} does not appear to be a file!".format(cipherFile))
        sys.exit(1)

    cipherText = open(cipherFile,"r").read()
    

    if(decryptSingleFile):
        print("Decrypting file {} with password {}, writing solution to {}".format(sys.argv[1], sys.argv[2], sys.argv[3]))
        textEnc = VigenereDecipher(cipherText,sys.argv[2],alphabet)
        file = open(os.path.join(sys.argv[3]),"w")
        file.write(textEnc)
    else:            
        kL = int(sys.argv[2])
        if(kL <= 0):
            print("Error! {} is not a valid pattern length!".format(kL))
            sys.exit(1)
        if(kL < 4):
            print("Error! As a key of length less than four is not likely, cracking is not supported!")
            sys.exit(1)
        
        cT = alignInColums(cipherText, kL)
        
        print("Finding most likely passwords with {} characters ...".format(kL)) 
        (pswd,kLikely) = getPasswords(cT, kL, letterFrequencyDistribution, alphabet, languageX)

        if( createLetterDistributionTableOnly == False ):
            print("Building password table ...") 
            pswds = buildPasswordList(kLikely,300) 
                   
            print("Decrypting cipher with most probable keys ...")
            VigenereDecipherPWList(cipherText, alphabet ,pswds,"./out")
        
            print("Generating summary pdf to {}".format(sys.argv[3]))
            generatePdf("./out", sys.argv[3])
            
    return 0    

if __name__ == '__main__':
    sys.exit(main())
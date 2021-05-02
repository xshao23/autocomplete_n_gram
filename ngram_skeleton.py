import math, random

################################################################################
# Part 0: Utility Functions
################################################################################

COUNTRY_CODES = ['af', 'cn', 'de', 'fi', 'fr', 'in', 'ir', 'pk', 'za']

def start_pad(n):
    ''' Returns a padding string of length n to append to the front of text
        as a pre-processing step to building n-grams '''
    return '~' * n

def ngrams(n, text):
    ''' Returns the ngrams of the text as tuples where the first element is
        the length-n context and the second is the character '''
    n_grams = []
    pad = start_pad(n)
    stack = []
    if n == 0:
        for i in text:
            tu = ("",i)
            n_grams.append(tu)
        return n_grams
    for i in pad:
        stack.append(i)

    for i in text:
        tu = ("".join(stack), str(i))
        n_grams.append(tu)
        stack.pop(0)
        stack.append(i)

    return n_grams

def create_ngram_model(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        model.update(f.read())
    return model

def create_ngram_model_interpolated(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    model.set_lambdas_2()
    print(model.lambdas)
    with open(path, encoding='utf-8', errors='ignore') as f:
        model.update(f.read())
    return model, model.lambdas

def create_ngram_model_lines(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            model.update(line.strip())
    return model

################################################################################
# Part 1: Basic N-Gram Model
################################################################################

class NgramModel(object):
    ''' A basic n-gram model using add-k smoothing '''

    def __init__(self, c, k):
        self.c = c
        self.k = k 
        self.vocab = set()
        self.n_grams_dict = dict() # let keys be context and elements stored be the element 
        

    def get_vocab(self):
        ''' Returns the set of characters in the vocab '''
        # li = []
        # a=set()
        # # for word in self.vocabs:
        # #   a.update(set(word))
        # #   # grams = n_grams(self.n, word)
        # #   # li.append(grams)
        # # return a
        # for value in self.n_grams_dict.values():
        #     for char in value.keys():
        #         a.add(char)

        return self.vocab

    def update(self, text):
        ''' Updates the model n-grams based on text '''
        self.vocab = self.vocab | set(text)
        n_grams_li = ngrams(self.c, text)
        for tup in n_grams_li:
            context, char = tup
            chars_in_context = self.n_grams_dict.get(context, dict())
            char_freqs = chars_in_context.get(char, 0)
            char_freqs+=1
            chars_in_context[char] = char_freqs
            self.n_grams_dict[context] = chars_in_context
        #self.vocabs.append(text)

        

    # probability with smoothing 
    # p(w_n|<context>) = (c(context,w_n)+k)/(c(context)+k|V|)

    def prob(self, context, char):
        ''' Returns the probability of char appearing after context '''
        # if context in self.n_grams_dict.keys():
        #     char_freqs_in_context = self.n_grams_dict[context]
        #     if char in char_freqs_in_context.keys():
        #         sum = 0
        #         for freq in char_freqs_in_context.values():
        #             sum += freq
        #         return char_freqs_in_context[char]/sum
        #     else:
        #         v = len(self.get_vocab())
        #         sum = 0
        #         for freq in char_freqs_in_context.values():
        #             sum += freq

        #         return (self.k/(sum+self.k*v)) 
        
        # return 1/len(self.get_vocab())
        if context in self.n_grams_dict.keys():
            char_freqs_in_context = self.n_grams_dict[context]
            sum = 0
            for freq in char_freqs_in_context.values():
                sum += freq
            freq = char_freqs_in_context.get(char, 0)
            result = (freq+self.k)/(sum+self.k*len(self.get_vocab()))
            return result
        else:
            return 1/len(self.get_vocab())


        pass

    def random_char(self, context):
        ''' Returns a random character based on the given context and the 
            n-grams learned by this model '''
        cdf = dict()
        vocab = list(self.get_vocab())
        prev_cdf = 0
        for i, char in enumerate(sorted(vocab)):
            pr = self.prob(context,char)
            prev_cdf += pr
            cdf[char] = prev_cdf 


        # if context in self.n_grams_dict.keys():
        #     chars_in_context = self.n_grams_dict[context]
        #     sum = 0 
        #     for freq in chars_in_context.values():
        #         sum += freq
        #     prev_cdf = 0

        #     for i, char in enumerate(sorted(chars_in_context.keys())):
        #         # print("char is  ",char)
        #         freq = chars_in_context[char]/sum
        #         # print("freq is %f" % (freq+prev_cdf))
        #         cdf[char] = freq+prev_cdf
        #         prev_cdf += freq

        #     prev_cdf = 0
        # else:
        #     vocabs = self.get_vocab();
        #     for i, char in enumerate(sorted(vocabs)):
        #         cdf[char] = (i+1)/len(vocabs)
        # if context == 'd':
        #     print(cdf)
       # print(self.n_grams_dict[""])
        _r = random.random()
        for value in sorted(cdf.values()):
           # print("value is "+str(value))
            if _r < value:
                for char, out_value in cdf.items():
                    if value == out_value:
                        return char

        pass

    def random_text(self, length):
        ''' Returns text of the specified character length based on the
            n-grams learned by this model '''
        text = ""
        context = start_pad(self.c)
        for i in range(length):
            char = self.random_char(context)
            # print("char is ", char)
            # print("context is ",context)
            if len(text) == 0:
                text = char
            else:
                text = text + char
            context = context[1:] + char
        return text

    def perplexity(self, text):
        ''' Returns the perplexity of text based on the n-grams learned by
            this model '''
        if (self.c != 0):
            padded_text = start_pad(self.c) + text  

        log_sum = 0
        for i in range(len(text)):
            r = 0 
            if (self.c != 0):
                context = padded_text[i:self.c+i]
            #print("context is ", context)
                char = padded_text[self.c+i]
            #print("char is ", char)
                r = self.prob(context, char)
            else:
                char = text[i]
                r = self.prob("", char)
            if (r==0):
                return float("inf") 
            #print("r is ",str(r))
            log_sum += math.log(r,10)

        return pow(10, float(-1/len(text))*float(log_sum))



        pass

################################################################################
# Part 2: N-Gram Model with Interpolation
################################################################################

class NgramModelWithInterpolation(NgramModel):
    ''' An n-gram model with interpolation '''

    def __init__(self, c, k):
        NgramModel.__init__(self, c, k)
        self.n_grams_dicts = [dict() for k in range(c+1)]# let keys be context and elements stored be the element 
        self.lambdas = [1/(c+1) for k in range(c+1)]
        

        #print(self.lambdas)
    # def get_vocab(self):
    #     a=set()
    #     tmp_dict = self.n_grams_dicts[0]

    #     for value in tmp_dict.values():
    #         for char in value.keys():
    #             a.add(char)

    #     return a
    #     pass

    def update(self, text):
        c = self.c 
        self.vocab = self.vocab | set(text)
        for i in range(c+1):
            #print("update i is %d" %i)
            n_grams_li = ngrams(i, text)
            tmp_dict = self.n_grams_dicts[i]
            #print("printing ngram list")
           # print(n_grams_li)
           # print("dictionary before update")
         #   print(tmp_dict)
            for tup in n_grams_li:
                context, char = tup
                #print("context is %s" %context)
                chars_in_context = tmp_dict.get(context, dict())
                char_freqs = chars_in_context.get(char, 0)
                char_freqs+=1
                chars_in_context[char] = char_freqs
                tmp_dict[context] = chars_in_context
          #  print("dictionary updated")
            #print(tmp_dict)
            self.n_grams_dicts[i] = tmp_dict
          #  print(self.n_grams_dicts)

    def prob(self, context, char):
        results = []#[0]*(self.c+1)
        context1 = ""
        for i in range(self.c+1):
            #print("i is %d" %i)
            tmp_dict = self.n_grams_dicts[i]
            #print(tmp_dict)
            result = 0
            if i>0:
                context1 = context[len(context)-i:len(context)]
            #print("context1 is %s " %context1)
            # need to change the length of context 
            if context1 in tmp_dict.keys():
                #print(context1)
                char_freqs_in_context = tmp_dict[context1]
                sum = 0
                for freq in char_freqs_in_context.values():
                    sum += freq
                freq = char_freqs_in_context.get(char, 0)
                result = (freq+self.k)/(sum+self.k*len(self.get_vocab()))
                results.append(result)
            else:
                result = 1/len(self.get_vocab())
                results.append(result)
        pr = 0
        #print("results is")
        #print(results)
        #print(self.lambdas)
        for j in range(len(results)):
            #print("j is ", str(j))
            pr += results[j]*self.lambdas[j]
        #print("pr is %f" %pr)
        return pr



        pass

    def set_lambdas_1(self):
        lambdas = [(k+1)**2 for k in range(self.c+1)]
        #print("lambdas is %s" %lambdas)
        lsum = 0
        lsum = sum(lambdas)
        self.lambdas = [i/lsum for i in lambdas]
        print(self.lambdas)

    def set_lambdas_2(self):
        l = self.lambdas
        coeff = 0.2
        if (len(l)>=4):
            l[-1] = l[-1] +coeff*l[0]
            l[0] = l[0]*(1-coeff)
            l[-2] = l[-2] + coeff*l[1]
            l[1] = l[1]*(1-coeff)
        self.lambdas = l
        print(self.lambdas)


################################################################################
# Part 3: Your N-Gram Model Experimentation
################################################################################
def train_n_gram_classifiers(path_to_train,c,k, interpolation):
    import glob
    train_sets = glob.glob(path_to_train+'/*.txt')
    n_gram_classifiers = dict()

    for textset in train_sets:
        label = (textset.split('\\')[-1]).split('.')[0]
        
        # just for now may parametrize it later 
        if interpolation:
            m = NgramModelWithInterpolation(c, k)
            m.set_lambdas_2()
        else:
            m = NgramModel(c, k)
        # set lambdas 
        
        
        try: 
            f = open(textset, encoding='utf-8', errors='ignore')
        except:
            f = open(textset, encoding="ISO-8859-1")
        for line in f.readlines():
            line = line.strip()
            if line !="":
                m.update(line)
                #print(line)
        f.close()
        n_gram_classifiers[label] = m 
    return n_gram_classifiers

def predict_country(n_gram_classifiers, city):
    min_country = "" 
    min_perplexity = float('inf')
    for key in n_gram_classifiers.keys():
        m = n_gram_classifiers[key]
        #print(m.perplexity(city))
        min_perplexity = min(m.perplexity(city), min_perplexity)
        if (min_perplexity == m.perplexity(city)):
            min_country = key
    return min_country

def predict_test_set(path_to_test, n_gram_classifiers):
    y_pred = []
    with open(path_to_test, encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            line = line.strip()
            if line !="":
                country = predict_country(n_gram_classifiers, line)
                y_pred.append(country)

    with open('test_labels.txt','w') as f:
        y_pred=list(map(lambda y: str(y)+'\n', y_pred))
        f.writelines(y_pred)

def predict_dev_set(path_to_dev, n_gram_classifiers):
    import glob
    dev_sets = glob.glob(path_to_dev+'/*.txt')
    y_pred = dict()
    y_true = dict()
    counter = 0
    sum = 0

    # filling value of y_true
    for i, textset in enumerate(dev_sets):
        label = (textset.split('\\')[-1]).split('.')[0]
        cities = []
        # just for now may parametrize it later 
        try: 
            f = open(textset, encoding='utf-8', errors='ignore')
        except:
            f = open(textset, encoding="ISO-8859-1")
        for line in f.readlines():
            line = line.strip()
            if line !="":
                y_true[line] = label
        f.close()

    for city in y_true.keys():
        y_pred[city] = predict_country(n_gram_classifiers, city)
        counter += 1
        if (y_pred[city] == y_true[city]):
            sum += 1

    return (sum/counter)*100

def perplexity_on_dev_file(path_to_dev,n_gram_model):
    try:
        f = open(path_to_dev, encoding='utf-8', errors='ignore')
    except:
        f = open(path_to_dev, encoding="ISO-8859-1")
    text = f.read()
    f.close()
    n_gram_model.update(text)
    return n_gram_model.perplexity(text)


if __name__ == '__main__':
    # m = NgramModelWithInterpolation(1, 0)
    # m.update('abab')
    # #print(m.get_vocab())
    # print("printing out probability")
    # print(m.prob('a', 'a'))
    # print(m.prob('a', 'b'))
    # m = NgramModelWithInterpolation(2, 1)
    # m.update('abab')
    # m.update('abcd')
    # #print(m.get_vocab())
    # print(m.prob('~a', 'b'))
    # print(m.prob('ba', 'b'))
    # print(m.prob('~c', 'd'))
    # print(m.prob('bc', 'd'))
    # m = NgramModel(0, 0)
    # m.update('abab')
    # m.update('abcd')
    # random.seed(1)
    # print([m.random_char('') for i in range(25)])
    tups = []
    # for c in range(4,4):
        # for k in range(1,1):
    c = 4
    k = 1
    model_set = train_n_gram_classifiers('train', c, k, True)
    acc = predict_dev_set("val", model_set)
    tup= (c, k, acc)
    tups.append(tup)
#        break
           #predict_test_set("cities_test.txt", model_set)  
           #print("c is %d, k is %d, accuracy is %f" %(c,k,acc))
    # model_set = train_n_gram_classifiers('train',4,1,True)
    # predict_test_set("cities_test.txt", model_set)

    with open('acc_inter.csv','w') as f:
        SS = list(map(lambda y: str(y)+'\n', tups))
        SS = [(y.replace("(","")).replace(")","") for y in SS]
        for i in range(len(SS)):
            f.writelines(SS[i])
            

    #uninterpolated file 
    # tupss = []
    # tupnyt = []
    # lambdas = []
    # c = 4
    # k = 1
    # m, m_lambdas = create_ngram_model_interpolated(NgramModelWithInterpolation, 'shakespeare_input.txt', c,k)
    # dev_file = "shakespeare_sonnets.txt"
    # print("c is %d, k is %d: perplexity of %s is %f "%(c, k, dev_file, perplexity_on_dev_file(dev_file, m)))
    # tup_SS = (dev_file, m_lambdas, perplexity_on_dev_file(dev_file, m))
    # tupss.append(tup_SS)
    # lambdas.append(m_lambdas)

    # dev_file = "nytimes_article.txt"
    # print("c is %d, k is %d: perplexity of %s is %f "%(c, k, dev_file, perplexity_on_dev_file(dev_file, m)))
    # tup_nyt = (dev_file, m_lambdas, perplexity_on_dev_file(dev_file, m)) 
    # tupnyt.append(tup_nyt)
    # print("****************************")
            
       

    # with open('perplexity_tab_interpol_new.csv','w') as f:
    #     SS = list(map(lambda y: str(y)+'\n', tupss))
    #     NYT = list(map(lambda y: str(y)+'\n', tupnyt))
    #     SS = [(y.replace("(","")).replace(")","") for y in SS]
    #     NYT = [(y.replace("(","")).replace(")","") for y in NYT]
    #     for i in range(len(SS)):
    #         f.writelines(SS[i])
    #         f.writelines(NYT[i])


 
    
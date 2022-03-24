import re
import sys
import collections


class Lexanalyzer:
    
    
    
    def __init__(self, file_name):
        #open the file and read all of it, put the file content into input.
        my_file = open(file_name, 'r')
        self.input = my_file.read()
        #create two global variables that holds lexeme and token.
        self.lexeme = None
        self.token = None
        self.flag = False;
        #keep track the line number.
        self.line_num = 1
        
        #create a ordered dictionary to hold every regex.
        self.tokens = collections.OrderedDict([])
        self.tokens['<progname>'] = '[A-Z][A-Za-z0-9]*'
        self.tokens['<program>'] = 'program\\b'
        self.tokens['<begin>'] = 'begin\\b'
        self.tokens['<end>'] = 'end\\b'
        self.tokens['<read>'] = 'read\\b'
        self.tokens['<write>'] = 'write\\b'
        self.tokens['<if>'] = 'if\\b'
        self.tokens['<then>'] = 'then\\b'
        self.tokens['<else>'] = 'else\\b'
        self.tokens['<while>'] = 'while\\b'
        self.tokens['<do>'] = 'do\\b'
        self.tokens['<comment>'] = '#.*(\\n|$)'
        self.tokens['<constant>'] = '[0-9]+'
        self.tokens['<assignment_operator>'] = ':='
        self.tokens['<relational_operator>'] = '<=|<>|<|>=|=|>'
        self.tokens['<multiplying_operator>'] = '[*/]'
        self.tokens['<adding_operator>'] = '[+-]'
        self.tokens['<left_paren>'] = '[(]'
        self.tokens['<right_paren>'] = '\\)'
        self.tokens['<variable>'] = '[a-z][A-Za-z0-9]*'
        self.tokens['<comma>'] = ','
        self.tokens['<semi_colon>'] = ';'
        self.tokens['<line>'] = '\\n'
    
        

    def lex(self):
        
        #get rid of the white space on the left side
        if (re.match(self.tokens['<line>'], self.input) != None):
            self.line_num = self.line_num +1
        self.input = self.input.lstrip()
        
        
        while True:
            #check if the input is empty, if it is empty, return 'EOF'
            if self.input != '':
                #look through all the tokens and see whether the input contains legal lexeme and return the assoicated token if it finds a match, if not, get rid of the first character and search again.
                for key in self.tokens:
                    
                    m = re.match(self.tokens[key], self.input)
                    
                    if m != None and key != '<line>' and key != '<comment>':
                        if self.flag and key == '<progname>':
                         key = '<variable>'
                        #since we do not want the parser to check progname again and mix up variable with it, we will set up a flag to check whether we have alreadgy gotten a progname.
                        if key == '<progname>':
                            self.flag = True
                        
                        self.input = self.input[m.end():]
                        self.lexeme = m.group()
                        self.token = key
                        print(self.lexeme)
                        print(self.token)
                        return self.token
                    #check if the program finds the \n or comment, if so, update line_num, then ignore this token
                    elif m != None and (key == '<line>' or key == '<comment>'):
                        self.input = self.input[m.end():]
                        self.line_num = self.line_num+1
                        break
                else:
                    self.lexeme = self.input[:1]
                    self.input = self.input[1:]
                    print('Error: Lexeme ' + self.lexeme + ' not recognized')
            else:
                self.token = 'EOF'
                return self.token
        return self.token
                
                
                
                
#methods that return allow the user outside to access the data in the global variable.
    def current_lexeme(self):
        return self.lexeme
        
    def current_token(self):
        return self.token

    def get_line(self):
        return self.line_num






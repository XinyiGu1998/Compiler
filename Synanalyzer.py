from Lexanalyzer import Lexanalyzer

class Synanalyzer:
    #constructor to set up the inital global variables we need to access throughout the program
    def __init__(self, lex1):
        self.lex1 = lex1
        #hold the token we expect to see but does not see in the user's program
        self.error_list = [];
        self.token = self.lex1.lex()
        self.program()
    
    
    #check if the token is what we want and then get next token, if not, add the expected token to the error list
    def check_token(self, *expected_token):
        
        for exp_token in expected_token:
            
            if self.token == exp_token:
              
                self.token = self.lex1.lex()
                break
        else:
            self.add_error(*expected_token)
            

    #set up the error message
    def add_error(self, *expected_token):
        for exp_token in expected_token:
            self.error_list.append('Error: current token=' + self.token + ', expected token=' + exp_token + ' at line ' + str(self.lex1.get_line()))


    #<program> ::= program <progname> <compound stmt>
    def program(self):
        self.check_token('<program>')
        
        self.check_token('<progname>')
        
        self.compound_stmt()
        while self.token != 'EOF':
            self.add_error('EOF')
            self.token = self.lex1.lex()

    #<compound stmt> ::= begin <stmt> {; <stmt>} end
    def compound_stmt(self):
        self.check_token('<begin>')
        self.stmt()
        while self.token == '<semi_colon>':
            self.token = self.lex1.lex()
            self.stmt()

        self.check_token('<end>')

    #<stmt> ::= <simple stmt> | <structured stmt>
    def stmt(self):
        if self.token == '<begin>' or self.token == '<if>' or self.token == '<while>':
            self.structured_stmt()
        elif self.token == '<variable>' or self.token == '<read>' or self.token == '<write>':
            self.simpl_stmt()
        else:
            self.add_error('<begin>', '<if>', '<while>', '<variable>','<read>','<write>')
    
    #<simple stmt> ::= <assignment stmt> | <read stmt> | <write stmt> | <comment>
        #comment is checked as token
    def simpl_stmt(self):
        if self.token == '<variable>':
            self.assignment_stmt()
        elif self.token == '<read>':
            self.read_stmt()
        elif self.token == '<write>':
            self.write_stmt()
        else:
            self.add_error('<variable>', '<read>', '<write>')

    #<assignment stmt> ::= <variable> := <expression>
    def assignment_stmt(self):
        self.check_token('<variable>')
        
        self.check_token('<assignment_operator>')

        self.expression()

    #check which structured stmt the user are using
    #<structured stmt> ::= <compound stmt> | <if stmt> | <while stmt>
    def structured_stmt(self):
        if self.token == '<begin>':
            self.compound_stmt()
        elif self.token == '<if>':
            self.if_stmt()
        elif self.token == '<while>':
            self.while_stmt()
        elif self.token == '<else>':
            self.token = self.lex1.lex()
            self.stmt()
        else:
            self.add_error('<variable>', '<read>', '<write>')
    
    #<read stmt> ::= read ( <variable> { , <variable> } )
    def read_stmt(self):
        self.check_token('<read>')
        
        self.check_token('<left_paren>')
        
        self.check_token('<variable>')
        
        
        while self.token == '<comma>':
            self.token = self.lex1.lex()
            self.check_token('<variable>')
    
        self.check_token('<right_paren>')
        
    #<write stmt> ::= write ( <expression> { , <expression> } )
    def write_stmt(self):
        self.check_token('<write>')
        self.check_token('<left_paren>')
        self.expression()
        while self.token == '<comma>':
            self.token = self.lex1.lex()
            self.expression()
            
        self.check_token('<right_paren>')
    #<if stmt> ::= if <expression> then <stmt> |
                    #if <expression> then <stmt> else <stmt>
    def if_stmt(self):
        self.check_token('<if>')
        
        self.expression()
        
        self.check_token('<then>')
        
        self.stmt()
    
        if self.token == '<else>':
            self.check_token('<else>')
            self.stmt()


    #<while stmt> ::= while <expression> do <stmt>
    def while_stmt(self):
        self.check_token('<while>')
        
        self.expression()
        
        self.check_token('<do>')
        
        self.stmt()
    
    #<expression> ::= <simple expr> |
                    #<simple expr> <relational_operator> <simple expr>
    def expression(self):
        self.simple_expr()

        if self.token == '<relational_operator>':
            self.token = self.lex1.lex()
            self.simple_expr()

    #<simple expr> ::= [ <sign> ] <term> { <adding_operator> <term> }
    def simple_expr(self):
        if self.token == '<adding_operator>':
            self.token = self.lex1.lex()
        
        self.term()

        while self.token == '<adding_operator>':
            self.token = self.lex1.lex()
            self.term()

    #<term> ::= <factor> { <multiplying_operator> <factor> }
    def term(self):
        self.factor()
        #check if it takes another multiply operator, if it has one, then next token must be factor.
        while self.token == '<multiplying_operator>':
            self.token = self.lex1.lex()
            self.factor()

    #<factor> ::= <variable> | <constant> | ( <expression> )
    def factor(self):
        if self.token == '<variable>' or self.token == '<constant>':
            self.token = self.lex1.lex()
        elif self.token == '<left_paren>':
            self.token = self.lex1.lex()
            self.expression()
            self.check_token('<right_paren>')
        else:
            self.add_error('<variable>', '<constant>', '<left_paren>')


#if the program works fine, then notice the user that there is no syntax error, if it has problems, print out the error messages.
    def print_error(self):
        if len(self.error_list) == 0:
            print('Program has no syntax error')
        else:
            for error in self.error_list:
                print(error)

    
        

    

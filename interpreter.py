#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

number = re.compile("[0-9]+")
identifier = re.compile("[^\s0-9]+[^\s]*")
string = re.compile("[\"\']+[\w0-9 ]+[\"\']+")

def print_words(env):
	for word in env["words"]:
		print(word, end=" ")
	print()

def op(env, operation):
	if len(env["stack"]) >= 2:
		b = env["stack"].pop()
		a = env["stack"].pop()
		env["stack"].append(operation(a, b))
	else:
		raise RuntimeError("Zasobnik nema dostatecne mnozstvi elementu")
		
def save_word(env):
	if len(env["remainingAtoms"]) == 0:
		word = input("->")
	else:
		word = env["remainingAtoms"][:1].pop()
		env["remainingAtoms"] = env["remainingAtoms"][1:]
		
	if identifier.match(word):
		word_declared = False
		expression = ""
		while not word_declared:
			if len(env["remainingAtoms"]) == 0:
				atoms = input("-> ").split(" ")
			else:
				atoms = env["remainingAtoms"]
				
			while len(atoms) != 0:
				atom = atoms[:1].pop()
				atoms = atoms[1:]
				if atom == ";":
					word_declared = True
					break
				else:
					expression += " " + atom
			env["remainingAtoms"] = atoms
	
		env["words"][word] = lambda env : eval_expression(expression, env)
	else:
		raise RuntimeError("Nazev slova neni validni identifikator")	

def cond(enviroment):
	while not "then" in env["remainingAtoms"]:
		enviroment["remainingAtoms"] += input("-> ").split(" ")
		
	if enviroment["stack"].pop():
		atom = ""
		while atom != "else" and atom != "then":
			atom = enviroment["remainingAtoms"][:1].pop()
			env["remainingAtoms"] = env["remainingAtoms"][1:]
			eval_atom(atom, enviroment)
			
		while atom != "then":
			atom = enviroment["remainingAtoms"][:1].pop()
			env["remainingAtoms"] = env["remainingAtoms"][1:]
	else:
		atom = ""
		while atom != "else":
			atom = enviroment["remainingAtoms"][:1].pop()
			env["remainingAtoms"] = env["remainingAtoms"][1:]
		while atom != "then":
			atom = enviroment["remainingAtoms"][:1].pop()
			env["remainingAtoms"] = env["remainingAtoms"][1:]
			eval_atom(atom, enviroment)

def dup(env):
	if len(env["stack"]) != 0:
		value = env["stack"].pop()
		for i in range(0, 2):
			env["stack"].append(value)
		
def swap(env):
	if len(env["stack"]) >= 2:
		a = env["stack"].pop()
		b = env["stack"].pop()
		env["stack"].append(a)
		env["stack"].append(b)

def drop(env):
	if len(env["stack"]) != 0:
		env["stack"].pop()

env = {
	"stack" : [],
	"words" : {
		"." : (lambda env : print("nil") if not env["stack"] else print(env["stack"].pop())),
		"WORDS" : print_words,
		"/" : lambda env : op(env, lambda x, y : x / y),
		"*" : lambda env : op(env, lambda x, y : x * y),
		"%" : lambda env : op(env, lambda x, y : x % y),
		"-" : lambda env : op(env, lambda x, y : x - y),
		"+" : lambda env : op(env, lambda x, y : x + y),
		">" : lambda env : op(env, lambda x, y : x > y),
		">=" : lambda env : op(env, lambda x, y : x >= y),
		"<" : lambda env : op(env, lambda x, y : x < y),
		"<=" : lambda env : op(env, lambda x, y : x <= y),
		"!=" : lambda env : op(env, lambda x, y : x != y),
		"if" : cond,
		":" : lambda env : save_word(env),
		"dup" : dup,
		"swap" : swap,
		"drop" : drop,
		"then" : lambda env : env
	},
	"remainingAtoms" : []
}

def eval_atom(atom, enviroment):
	if number.match(atom):
		enviroment["stack"].append(int(atom))
	elif string.match(atom):
		enviroment["stack"].append(atom)
	elif identifier.match(atom):
		if atom in enviroment["words"]:
			enviroment["words"][atom](enviroment)
		else:
			raise RuntimeError("Slovo " + atom + " nebylo nalezeno")
		

def eval_expression(expression, enviroment):
	enviroment["remainingAtoms"] = expression.split(" ")
	while len(enviroment["remainingAtoms"]) > 0:
		atom = enviroment["remainingAtoms"][:1].pop()
		enviroment["remainingAtoms"] = enviroment["remainingAtoms"][1:]
		eval_atom(atom, enviroment)

def repl():
    while True:
        expression = input('> ')
        eval_expression(expression, env)

if __name__ == '__main__':
	repl()

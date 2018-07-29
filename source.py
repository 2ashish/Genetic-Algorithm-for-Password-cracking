import sys
import random
import string

def fitness(password,test_word):
	score=0
	if (len(password)!=len(test_word)):
		print("length do not match")
		return
	else :
		for i in range(len(password)):
			if(password[i]==test_word[i]):
				score+=1

		return score*100/len(password)

def new_word(length):
	word = ""
	for i in range(length):
		word+=(random.choice(string.ascii_letters + string.digits))					# if change here then change in mutate also
	return word

def get_first_gen(pop_size,length):
	pop = []
	for i in range(pop_size):
		pop.append(new_word(length))
	return pop

def pop_fitness(pop,password):
	pop_fit = {}
	for i in pop:
		pop_fit[i] = fitness(password,i)
	return sorted(pop_fit.items(), key = lambda t: t[1], reverse = True)

def select_pop(pop_sort,best ,lucky,pop_size):
	next_gen = []
	for i in range(best):
		if(i>=len(pop_sort)):
			next_gen.append(random.choice(pop_sort)[0])
		else:
			next_gen.append(pop_sort[i][0])
	for i in range(lucky):
		next_gen.append(random.choice(pop_sort)[0])
	random.shuffle(next_gen)
	return next_gen

def create_child(parent1,parent2):
	child = ""
	for i in range(len(parent1)):
		if(random.random()>0.5):
			child+=parent1[i]
		else :
			child+=parent2[i]
	return child

def create_children(parents):
	next_pop = []
	for i in range(int(len(parents)/2)):
		for j in range(4):			# 4 children per couple so population remain same
			next_pop.append(create_child(parents[i],parents[len(parents)-1-i]))
	return next_pop

def mutate(pop,chance):
	for i in range(len(pop)):
		if(random.random()*100<chance):
			k = random.randint(0,len(pop[0])-1)
			word = ""
			if(k!=0):
				word+=pop[i][:k]
			word+=random.choice(string.ascii_letters + string.digits)+ pop[i][k+1:]
			pop[i]=word
	return pop

password = sys.argv[1]				# correct password
pop_size = int(sys.argv[2])			# population size
best_candidates = int(sys.argv[3])	# number best candidate to select for next gen
lucky_candidates = int(sys.argv[4])	# number of lucky candidate to select
# best + lucky should be 50% of population size
mutation_percent = int(sys.argv[5]) # percentage of populations undergoes mutation
max_gen = int(sys.argv[6])			# max number of generation to simulate

# print(password)
# print(fitness(password,"abc"))
# print(new_word(20))

pop = get_first_gen(pop_size,len(password))

for i  in range(max_gen):
	pop_sort = pop_fitness(pop,password)
	# if(i%10==9):
	# 	print(i,pop_sort[0][1],pop_sort[0][0],len(pop_sort))
	if(pop_sort[0][1]==100.0):
		break
	next_parents = select_pop(pop_sort,best_candidates,lucky_candidates,pop_size)
	next_pop = create_children(next_parents)
	next_pop = mutate(next_pop,mutation_percent)
	pop = next_pop

print("password is:",pop_sort[0][0],"generation:",i,"number of attempts:",i*pop_size)
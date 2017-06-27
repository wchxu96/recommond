import numpy as np
import pandas as pd
import math
from operator import itemgetter

def getData(path):
	ratings = pd.read_csv(path)
	return ratings

def getData_np(path):
	ratings = np.loadtxt(path)
	return ratings
#user similarity
def UserSimilarity(ratings):
	item_users = dict()
	rating_group_by_movieId = ratings.groupby('movieId')#use movieId to get the item user grouped
	for key in ratings['movieId'].unique():
		item_users[key] = rating_group_by_movieId.get_group(key)
	C = dict()
	N = dict()
	for Item in item_users:
		user_list = list(set(item_users[Item]['userId']))
		for user in user_list:
			if user not in N:
				N[user] = 1
				C[user] = dict()
			else:
				N[user] += 1
			for user_other in user_list:
				if user == user_other:
					continue
				if user_other not in C[user]:
					C[user][user_other] = 1
				else:
					C[user][user_other] += 1	
	for user in C:
		for other_user in C[user]:
			C[user][other_user] /= math.sqrt(N[user] * N[other_user])
	return C

def recommond(user,C,ratings,K):#provide user with recommondation
	rank = dict()
	interacted_items = list(ratings.groupby('userId').get_group(user).ix[:,'movieId'])
	for other_user,user_co in sorted(C[user].items(),key=lambda d:d[1],reverse=True)[:K]:
		for item in list(ratings.groupby('userId').get_group(other_user).ix[:,'movieId']):
			if item in interacted_items:
				continue
			if item not in rank:
				rank[item] = 0
			rank[item] += user_co * ratings.loc[(ratings.userId==other_user) & (ratings.movieId==item),'rating'].values[0]
	return rank

def main():
	'''
	path = './data/ratings.csv'
	ratings = getData(path)
	C = UserSimilarity(ratings)
	user = input('Enter user Id: ')
	if user not in range(1,672):
		print "user not in list ,exit!"
		exit(0)
	else:
		item_list = sorted(recommond(user,C,ratings,30).items(),key=lambda d:float(d[1]),reverse=True)[:10]
		print "recommond 10 items:"
		print "item        item_score"
		for item,item_score in item_list:
			print "%d        %f" %(item,float(item_score))
	'''
	path = './data/filmtrust/ratings.txt'
	ratings = getData_np(path)
	itemsimilarity = ItemSimilarity(ratings)
	user = input('Enter user Id: ')
	if user not in range(1,1509):
		print "user not in list ,exit!"
		exit(0)
	rec = recommondByItem(ratings,itemsimilarity,user,60)
	item_list = sorted(rec.items(),key=lambda d:float(d[1]),reverse=True)[:10]
	print "recommond 10 items:"
	print "item        item_score"
	for item,item_score in item_list:
		print "%d        %f" %(item,float(item_score))
	

#item similarity
#it is very big that I cannot afford the memory:) so I changed the dataset named filmtrust
def ItemSimilarity(ratings):
	#similarity = np.
	# first count the user and the item
	# ratings is a numpy array
	count_user = np.unique(ratings[:,0])
	count_item = np.unique(ratings[:,1])
	N = dict()
	try:
		similarity_matrix = np.zeros((count_item.shape[0],count_item.shape[0]))
	except MemoryError:
		print "Oh,too much data to process,try to use a little dataset"
	item_users = dict()
	for unique_key in count_user:
		item_slice = ratings[ratings[:,0] == unique_key]
		#print item_slice[:,1]
		item_users[unique_key] = list(item_slice[:,1])
	for user,item_list in item_users.items():
		for item in item_list:
			if int(item) not in N:
				N[int(item)] = 0
			N[int(item)] += 1
			for other_item in item_list:
				if item == other_item:
					continue
				similarity_matrix[int(item) - 1][int(other_item) - 1] += 1
	for i in range(count_item.shape[0]):
		for j in range(count_item.shape[0]):
			similarity_matrix[i,j] = similarity_matrix[i,j] / (math.sqrt(N[i+1] * N[j+1]))
	return similarity_matrix

#each user has interest in:)
	#for item in item_users:

def recommondByItem(ratings,similarity_matrix,user,K):
	rank = dict()
	ru = ratings[ratings[:,0] == user][:,1]
	for item in list(ru):
		#for other_item in np.unique(ratings[:,1]):
		#select K most similar item with item
		idx = np.argpartition(similarity_matrix[int(item) - 1,:],-K)[-K:]
		#print idx[0]
		for other_item in list(idx):
			if (other_item + 1) in list(ru):
				continue
			if (other_item+1) not in rank:
				rank[other_item + 1] = 0
			user_res = ratings[ratings[:,0] == user]
			item_res = user_res[user_res[:,1] == item]
			rank[other_item + 1] += similarity_matrix[int(item) - 1][int(other_item)] * item_res[0,2]
	return rank
			
if __name__ == '__main__':
	main()	
			
			
		
		 
		
	
	

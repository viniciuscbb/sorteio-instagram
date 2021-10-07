from instagram_private_api import Client
import random
import re

user     = ''
password = ''

api = Client(user, password)

print('Listando usuários que seguem @botfreeiq')
UUID = api.generate_uuid() # Necessário para a API
followers = api.user_followers(api.authenticated_user_id, rank_token=UUID)['users'] # Lista de usuários que seguem o perfil do Neps.
followers = [follower['pk'] for follower in followers] # Mas queremos uma lista apenas com o ID dos usuários

POST_CODE =  "CUlgVPRs1oe"
n_comments = 8478
post_id = None

feed = api.self_feed() # Primeiro pegamos todas as postagens no nosso feed.
for item in feed['items']: # Iteramos em cada postagem.
	if item['code'] == POST_CODE: # Se a postagem tem _code_ igual a POST_CODE
		post_id = item['id'] # Salvamos o ID dessa postagem na variável post_id
		break

users_valid_comments = []

print(f'Carregando comentários do post www.instagram.com/p/{POST_CODE}')
comments = api.media_n_comments(post_id, n=n_comments) # Vamos pegar os 500 primeiros comentários do nosso post

post_likes = api.media_likers(post_id)

print(f'Carregado {n_comments} comentários!')

# Tiramos os comentários repetidos
newlist = comments
for comment in comments:
    match = re.findall(r"(@\w*)", comment['text'])
    
    for x, comment2 in enumerate(newlist):	    
        match2 = re.findall(r"(@\w*)", comment2['text'])
        if match == match2:
            newlist.remove(newlist[x])

comments = newlist
for comment in comments:	    
    match = re.findall(r"(@\w*)", comment['text'])

    for like in post_likes['users']:
        # Se o usuário realmente marcou uma pessoas, segue o perfil do BotFree e se deu like no post, adicionamos ele nos comentários válidos
        if(len(match) >= 1 and comment['user_id'] in followers and comment['user']['pk'] == like['pk']):
            users_valid_comments.append(comment['user_id'])

print(f'{len(newlist)} comentários válidos segundo as regras!\n')

random.shuffle(users_valid_comments)
winners = set()

print(input('Aperte enter para continuar '))

i = 0
while len(winners) < 3: # Enquanto nosso conjunto de vencedores tem menos que 5 pessoas
	if users_valid_comments[i] not in winners: # Se a pessoa ainda não está no nosso conjunto de vencedores adicionamos ele
		winners.add(users_valid_comments[i])
	i += 1 # Vamos para o próxima pessoa

print('Parabéns aos vencedores!!!\n=========== VENCEDORES ===========')
n = 0
for winner_id in winners: # Para cada vencedor
    n += 1
    winner = api.user_info(winner_id)['user'] # Use a API para pegar informações detalhadas dessa pessoa
    print(f"| {n}º {winner['full_name']}  @{winner['username']}") # Imprima nome completo e nome de usuário no Instagram.

print('==================================')
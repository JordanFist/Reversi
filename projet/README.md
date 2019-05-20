# Reversi

##Recherche:
La recherche est faite par un algorithme minmax avec élagage alpha-beta et iterative deepening. Pour les 3 premiers coups, le groupe a implémenté des ouvertures (qui sont expliqués ensuite).

Après, pour chaque coup, l'algorithme fait une recherche en profondeur 1. Sachant que le temps est exponentiell en rélation à la profondeur, nous cherchons le x tel que x**profondeur = temps passé. Avec cette valeur x, nous estimons le temps pour faire profondeur+1 et, si cette valeur ne dépasse pas un limite pré-établi, la recherche recommence avec profondeur +1. Encore, pour essayer de s'approcher plus d'une bonne estimation, nous divisons le temps calculé passé à la profondeur actuel pour l'estimation faite avant. Le résultat est un coefficient pour lequel nous multiplierons la prochaine estimation.

Le temps limite donné pour chaque recherche change en fonction du tour. Au tout début, le limite est 6 secondes, lors qu'ils existent plusieurs possibilités et elles ne sont pas forcement très intéressants à être explorées. Comme le groupe a observé que le temps de calcul commence à diminuire environ au 70-ème coup, à partir de ce moment-là le temps devient le résultat de la division du temps que nous reste par la quantité de tours encore à jouer. Il faut remarquer que ce n'est pas possible d'être sur de la quantité de coups à jouer, lors que l'adversaire peut nous faire gagner un tour ou le contraire, mais les tests ont montré que cette approximation fonctionne bien.

Pour mieux profiter de l'iterative deepening, à chaque fois que l'algorithme arrive à une valeur heuristique, cette valeur est stocké dans un dictionnaire. Pour identifier chaque plateau dans ce dictionnaire, nous utilisons la chaîne de caractères qui décrit l'état actuel du plateau. Avec cette information, à chaque fois qu'il faut parcourir les coups possibles, avant le faire nous cherchons la valeur stocké pour cet état et puis nous jouons les coup de façon ordonné (différemment pour min et max) pour que l'elagage alpha-beta élage le maximum de coups possible. Finalement, pour les coups dont nous n'avons pas de valeur stocké, un score standard est donné de façon que les coups inconnus soient exploré en premier. Grace à cette téchnique, nous n'allons jamais élaguer un coup qui n'a été pas exploré.


##Openings:
Ce fichier a pour but d’obtenir un dictionnaire d’ouverture dans le lequel l’IA aurait juste à regarder si son plateau est le même que celui enregistré et à jouer le coup que l’ouverture lui conseil de jouer.

Pour faire ces ouvertures, nous nous sommes inspirés de parties réelles et d’IA déjà existante du jeu Othello. Le dictionnaire crée nous permet de jouer jusqu’à la profondeur 3 sans avoir à lancer l’algorithme de recherche et nous fait donc gagner du temps sur les premiers coups déjà bien étudié par les théoriciens.

Pour faciliter les affectations plateau <-> move, nous avons également pris en compte les symétries du plateau initial c’est à dire Y = X, Y = -X et la combinaison de ces 2 symétries.

##Heuristiques:
Afin de tirer profit de notre algorithme de recherche, il est
heurisitique(board)= poids_mobilité(tour_restants(board))* mobilité(board)
    + poids_coins(tour_restants(board)) * coins(board)
    + poids_position(tour_restants(board)) * positions(board)
    + poids_disques(tour_restants(board)) * disques(board)

avec:
-mobilité(board) retourne une valeur entre 0 et 1 représentant la différence de mobilité entre le joueur courant et son adversaire.
-poids_mobilité(n) cette fonction est croissante en le nombre de tours restant car on considère que la mobilité est plus importante au début de la partie qu'à la fin
-coins(board) retourne une valeur entre 0 et 1 en fonction de combien de coins sont pris par le joueur
-poids_coins() cette fonction retourne une constante car les coins sont toujours aussi importants
-position() cette fonction applique un masque associant à chaque case du plateau un poids statique représentant l'avantage que la prise de cette case présente pour le joueur. Elle retourne une valeur entre 0 et 1.
-poids_position() Cette fonction retourne une constante car l'importance des emplacements sur la grille est la même tout au long de la partie.
-disques() Retourne une valeur entre 0 et 1 représentant la domination du joueur courant par rapport à l'autre.
-poids_disques(n) cette fonction est décroissante en le nombre de tours restants.


Le code est disponible à https://github.com/JordanFist/Reversi
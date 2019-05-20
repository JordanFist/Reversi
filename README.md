# Reversi

##Openings: 
Ce fichier a pour but d’obtenir un dictionnaire d’ouverture dans le lequel l’IA aurait juste à regarder si son plateau est le même que celui enregistré et à jouer le coup que l’ouverture lui conseil de jouer.

Pour faire ces ouvertures, nous nous sommes inspirés de parties réelles et d’IA déjà existante du jeu Othello. Le dictionnaire crée nous permet de jouer jusqu’à la profondeur 3 sans avoir à lancer l’algorithme de recherche et nous fait donc gagner du temps sur les premiers coups déjà bien étudié par les théoriciens.

Pour faciliter les affectations plateau <-> move, nous avons également pris en compte les symétries du plateau initial c’est à dire Y = X, Y = -X et la combinaison de ces 2 symétries.
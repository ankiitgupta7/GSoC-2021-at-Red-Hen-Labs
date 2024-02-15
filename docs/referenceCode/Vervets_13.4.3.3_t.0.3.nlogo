extensions [ sound ]

turtles-own [ energy ]
patches-own [ patchtype food]


breed [ vervets vervet]
breed [ snakes snake ]
breed [ leopards leopard ]
breed [ hawks hawk ]
breed [ trees tree]
breed [ bushes bush]
breed [ stones stone]

vervets-own [ strat_prob type_pred type_prob type_anxiety mytype_anxiety myfear flockmates nearest-neighbor myanxiety anxiety mystrategy posct predct negct strct alert
   thungera thungerm learnct learncti zeroct alertct negcta onect twoct threect onenegct twonegct threenegct eaten anx starve patchcount matrix anx_index hun_index anx_cap]  

;; strat_prob of form [0.0 0.33 0.33 0.33]; prob of strategy 0, prob of strategy 1 ...; currently stratgy 0 is a 'dummy strategy' 
        ;; (kludge to make strategy 1 match index 1, ... since index 1 refers to the second position in a list)
;; type_pred of form [[0 0 0] [0 0 0] [0 0 0] [0 0 0]] [patchtype1[predatortype] ... patchtype4[predator type]]; number of type of predators encountered per patchtype
;; type_prob of form [0.5 0.5 0.5 0.5]; probability of going to grass, bush, stone, tree area
;; type_anxiety is of form [0 0 0 0]; anxiety for each type of predators if vervet saw all predators of that type that could possibly have been seen by the vervet
;; anxiety is a variable for the anxiety level based on all predators that could have been seen by a vervet 
;; mytype_anxiety is of form [0 0 0 0] ; anxiety level for each patchtype based on number of predators actually seen by a vervet in that patchtype
;; myanxiety is a variable for the anxiety level based on all predators that were seen by a vervet
;; myfear is a variable
;; flockmates is the collection of vervets that is used in flock movement
;; nearest-neighbor
;; mystrategy is the current strategy for a vervet
;posct is the number of times a vervet uses predatorcheck
;predct is number of times predatorcheck spots predator
;negct count for negative learning
;strct number of times a(ny) strategy is used
;eaten number of times predators reach vervet
;anx experimental anxiety placeholder
;starve number times vervet's energy falls to zero
;matrix holds vervet strategy for different combinations of anxiety and hunger.
;anx_index anxiety level 0 1 2
;hun_index hunger level 0 1 2
;anx_cap records highest seen anxiety

globals [danger nearby metabolism grassprob bushprob treeprob stoneprob strat1prob strat2prob strat3prob sumgrass sumstone sumbush sumtree sumhawk sumsnake sumleopard 
grasstype bushtype stonetype treetype leopardpred hawkpred snakepred areaXY fear mean_type_anxiety mean_anxiety mean_myanxiety mean_mytype_anxiety foodstock Numvervets 
tfeara tavoid avgalerted numstr1 numstr2 numstr3 str1sxs str2sxs str3sxs mean_fear mean_anx mean_hunger mean_eaten matrix00 matrix01 matrix02 matrix10 matrix11 matrix12 
matrix20 matrix21 matrix22]
;;grassprob  mean probability of going to grass area 
;;bushprob
;;treeprob
;;stoneprob
;;strat1prob  mean probability of doing strategy 1
;;strat2prob 
;;strat3prob
;;sumgrass total number of grass events
;;sumstone
;;sumbush
;;sumtree
;;sumhawk total number of hawk encounters
;;sumsnake
;;sumleopard
;;mean_type_anxiety  mean possible anxiety, based on all predator encounters (not sure; need to check this)
;;mean_myanxiety  mean anxiety of vervets
;;mean_mytype_anxiety
;;one/two/threect counts total number of experiences while using respective number strategy
;;one/two/threenegct counts total number of negative experiences while using respective number strategy
;;alertrad is the radius in which the vervets can access other vervets' alert variable
;;avgalerted is used to record and display the average of vervet variable alertct, the counter for the # times each vervet has been alerted
;;numstr1,2,3 records the number of vervets for which the leading strategy by probability is 1/2/3
;;str1/2/3sxs records the success rate of each strategy among the vervets for which it leads in probability

to setup
  ;; (for this model to work with NetLogo's new plotting features,
  ;; __clear-all-and-reset-ticks should be replaced with clear-all at
  ;; the beginning of your setup procedure and reset-ticks at the end
  ;; of the procedure.)
  __clear-all-and-reset-ticks
  set-globals
  ;set alertrad 9 ;now set by user
  ;set alertct 0 ;changed to vervet var
  ;set alerts 0
  set-global-counters
  landscape-location
  setup-area                                       ;; sets up a Moore neighborhood (square) for a resource
  setup-breeds                                     ;; sets up breeds of turtles, including trees, bushes and stones
  create-landscape                                 ;;create the lanscape with Moore neighborhoods for trees, bushes and stones and populate each neighborhood
  create-animals                                   ;; create vervets, hawks, snakes and leopards
;  do-plotting
  ask vervets [generate-random-matrix]
  count-matrix
end


to go
  tick
  vervet-movement
  predator-movement
  color-environment
  
  do-plotting
  
  update-variables 
  update-statistics
  count-matrix
end

to count-matrix
  set matrix00 mean [item 0 item 0 matrix] of vervets
  set matrix01 mean [item 1 item 0 matrix] of vervets
  set matrix02 mean [item 2 item 0 matrix] of vervets
  set matrix10 mean [item 0 item 1 matrix] of vervets
  set matrix11 mean [item 1 item 1 matrix] of vervets
  set matrix12 mean [item 2 item 1 matrix] of vervets
  set matrix20 mean [item 0 item 2 matrix] of vervets
  set matrix21 mean [item 1 item 2 matrix] of vervets
  set matrix22 mean [item 2 item 2 matrix] of vervets
end







  
to-report check-for-food                            ;; report if a patch has food
  report [food] of patch-here
end



;;============================VERVET PROCEDURES===========================

to vervet-movement
  ask vervets 
    [ decay-energy                                           ;; metabolic cost
      act-on-internal-state                                  ;; all actions based on internal state of vervet
      if energy <= 0 [set starve starve + 1
        generate-random-matrix
        set energy metabolism]                   ;;adjust decision matrix
      countpatches
      ;show myanxiety show mytype_anxiety
       ;if energy = 0 [play-note "TRUMPET" 60 64 0.5 die]
       ] ;; temporary as only vervets move at the moment
end

to countpatches
  let newcount item mypatchtype patchcount + 1
  set patchcount replace-item mypatchtype patchcount newcount
end

to act-on-internal-state
  ifelse anxiety-type = 1 [set anx myanxB] [
    ifelse anxiety-type = 2 [set anx myanxB2] [
      ifelse anxiety-type = 3 [set anx myanxB3] [
        user-message "Anxiety-type not set"]
    ]
  ]
  set anx_cap anx_cap * (1 - anxiety_decay)
  if (ticks mod 10 = 0) [set anx_cap 0]
  if anx > anx_cap [set anx_cap anx]
  determine-index
  ifelse mymove = 1 [vector-move] [
   ifelse mymove = 0 [hunger-action]
   [user-message "Mymove malfunction"] 
  ]
end

to hunger-action                                    ;; turtle procedure
  ask self [set thungera thungera + 1]
  ifelse check-for-food = 0                         ;; if there is no food ...
    [hunger-move]                                   ;; then move ...
    [eat-food]                                      ;; else eat food
end

to fear-action                                      ;; vervet procedure 
    fear-move                                       ;; move out of fear
    set tfeara tfeara + 1
end

;-----------------------------------------------------------vervet move actions

to avoid-predator      ;; procedure to avoid a predator
  decay-energy         ;; it costs energy to move 
  fear-move            ;; move out of fear
  set tavoid tavoid + 1
end

to fear-move                                          ;; procedure to move out of fear
  ;if mystrategy = 0 [set mystrategy select-strategy]  ;; if currently no strategy, select a strategy for moving out of fear, otherwise use last strategy
  set mystrategy select-strategy                      ;; set strategy for moving out of fear (remember past strategies via learning)
  if mystrategy = 1 [set onect onect + 1]
  if mystrategy = 2 [set twoct twoct + 1]
  if mystrategy = 3 [set threect threect + 1]
  strategy-move                                       ;; move according to the selected strategy
  predator-check
  set strct strct + 1   ;update vervet's total strategy moves
  ;decay-fear                                          ;; decay fear since vervet moved, so less fearful
;  if select-strategy = 1                             ;; these commented out statements replace by strategy-move procedure
;    [move-strategy1] 
;  if select-strategy = 2
;    [move-strategy2] 
;  if select-strategy = 3
;    [move-strategy3] 
  set mystrategy 0                                    ;;reset to 0; strategies are not remembered except via learning                 
end

to hunger-move                     ;; procedure to move due to hunger
;  color-anxiety                    ;; color according to level of anxiety
  ask self [set thungerm thungerm + 1]
  ifelse mypatchtype != grasstype  ;; if not in the grass
     [move-to-grass-area]          ;; then move to grass...
     [move-action]                 ;; otherwise just move (move-action)
;  ifelse mypatchtype = grasstype 
;    [move-action 
;    ifelse checkforpredators  ;;checkforpredators resets the fear level, uses flock move
;        [avoid-predator]
;        [if energy < metabolism [grow-energy decay-anxiety]]] ;;no predator, so eat if hungry, lose anxiety
;    [if myfear < hunger-level [move-to-grass-area]] ;;no predator, move to grass, lose anxiety; jumps out of safe area (correct)
end

;----------------------------------------------------------strategy

to strategy-move                                      ;; procedure to move according to the strategy selected
  ifelse mystrategy = 1                               ;; if strategy is strategy 1 ...
    [set color yellow move-strategy1]                 ;; set yellow to denote strategy 1 and use strategy 1 to move ...
    [ifelse mystrategy = 2                            ;; otherwise, if strategy is strategy 2 ...
      [set color blue move-strategy2]                 ;; set blue to denote strategy 2 and use strategy 2 to move ...
      [set color gray move-strategy4]                 ;; otherwise set gray to denote strategy 3 and use strategy 3 to move
     ]
end

to-report select-strategy                 ;; procedure for selecting a strategy
  let p random-float 1                    ;; initialize p to be a random number < 1
  let psum item 1 strat_prob              ;; strat_prob a vector of probabilities: [strategy 0, strategy 1, strategy 2, strategy 3]
                                          ;; set psum to be the probability of strategy 1
  if p < psum [report 1]                  ;; if p < psum, select strategy 1
  set psum psum + item 2 strat_prob       ;; otherwise increment psum by the probability of strategy 2
  if p < psum [report 2]                  ;; if p < psum, select strategy 2
  report 3                                ;; otherwise, select strategy 3
end

to move-strategy1                                     ;; move using strategy 1
  random-move 6                                       ;; randomly move a distance of 6
  ;show learncti
  ;show strat_prob
end

to move-strategy2                                  ;; move using strategy 2                                   
  move-to-safearea                                 ;; move to a safe area regardless of current location
end

to move-strategy3                                  ;; move using strategy 3                                     
  ifelse mypatchtype = grasstype                   ;; if in grass ... 
    [move-to-safearea]                            ;; move to safearea ...
    ;[if checkforpredators [move-to-safearea]]     ;; otherwise check for predators and move if there are predators
    ;[if checkforpredators []]
    [move-in-safe-area]
end

to move-strategy4                                 ;;predator-specific strategy
  ifelse any? hawkshere
  [go-to-area item bushtype areaXY]
  [ifelse any? snakeshere
  [go-to-area item stonetype areaXY]
  [if any? leopardshere
  [go-to-area item treetype areaXY]
  ;[set learncti learncti + 1]
  ]]
end

;------------------------------------------------------------------------------------learning

to-report negative-learn [probability]              ;; negative learning
   report probability - (b * probability)           ;; report p - b*p, b the weighting factor for negative learning
end

to-report positive-learn [probability]              ;; positive learning
  report (probability + a * (1 - probability))      ;; report p = p + a*(1-p), a the weighting factor for positive learning
end

to negative-learn-patchtype [thepatchtype]                          ;; procedure for negative learning patchtype
  let newprob negative-learn (item thepatchtype type_prob)
  ask self [set type_prob replace-item thepatchtype type_prob newprob 
    set type_prob normalize-prob-list type_prob
    ]                                                               ;; update area learning probabilities
end

to negative-learn-strategy                                          ;; procedure for negative learning strategy
  if mystrategy > 0 [set negct negct + 1]  ;update count of times used
  set negcta negcta + 1
  let newprob negative-learn (item mystrategy strat_prob)
  if newprob < 0.1 [set newprob 0]
  let deltaprob ((item mystrategy strat_prob) - newprob) / 2
  ask self [set strat_prob replace-item mystrategy strat_prob newprob
    set strat_prob normalize-prob-list-omit1 strat_prob 0 deltaprob           ;; make list of numbers into probabilities after it has been modified
if mystrategy = 1 [set onenegct onenegct + 1]
if mystrategy = 2 [set twonegct twonegct + 1]
if mystrategy = 3 [set threenegct threenegct + 1]
  ]                                                                 ;; update strategy learning probabilities
end

to positive-learn-strategy                                          ;; procedure for positive learning strategy
;show myanxiety
set learnct learnct + 1
;  if myanxiety > 40                                               ;; only positive learn when already have high anxiety; 40 is a trial value
  let newprob positive-learn (item mystrategy strat_prob)
    let deltaprob ((item mystrategy strat_prob) - newprob) / 2    ;;deltaprob is negative
    ;show deltaprob
    ;show strat_prob
  ask self [set strat_prob replace-item mystrategy strat_prob newprob
    set strat_prob normalize-prob-list-omit1 strat_prob 0 deltaprob           ;; make list of numbers into probabilities after it has been modified
    ;show strat_prob
    ;show mystrategy
  ]                                                                 ;; update strategy learning probabilities
end

;--------------------------------------------------------------------------------------

to predator-check                                          ;; procedure to check for predators
  ifelse checkforpredators [                                ;; if check for predators is true ...
      set myfear fear
      if mystrategy > 0 [negative-learn-strategy]
      color-anxiety                         ;; avoid predators, color anxiety level ...
    set predct predct + 1]                     
    [decay-anxiety                                         ;; otherwise just decay anxiety (since no predators were found) 
    if mystrategy > 0                                      ;; only positive learn when vervet has just used a strategy and did not find any predators
      [positive-learn-strategy]      ;; CHECK to see if one can get here without using a strategy; if so, should not positive learn
      set alert 0                   ;;switch alert var off if no predators found
      decay-fear
      decay-anx
     ] 
    if mystrategy = 0 [set zeroct zeroct + 1]
    set posct posct + 1   ;update count of times used
                                                       ;; update strategy probability, positive learning
end

;--------------------------------------------------------------------------basic utilities

to move-in-safe-area            ;; procedure to move in safe area (not currently used -- see above procedure)    
 ;decay-fear                    ;; fear decays 
 random-move-in-area            ;; randomly move in the safe area
end



to move-to-grass-area                   ;;move to grass area via random moves, may need to be modified
  ;move-action 
  random-move 5                         ;; randomly move distance 5
  if mypatchtype != grasstype 
    [move-to-grass-area]                ;; if not in grass area, repeat
    ;[predator-check]                    ;; now in grass area, check for predators
end

to move-action              ;; procedure for moving
  ifelse flock              ;; if flock is true ...
    [flock-move]            ;; use flock move ...
    [random-move 2]         ;; otherwise randomly move distance 2
end

to move-to-patch [thepatch]    ;; procedure to move to a patch
  move-to thepatch             ;; move to the patch
  ;predator-check               ;; check for predators REMOVE
end

to flock-move                ;; procedure for flock move
  flock-movement 1           ;; flock move distance 1
  ;flock-movement random 1
  ;predator-check             ;; check for predators REMOVE
end

to random-move [step]         ;; general purpose procdure for random movement of a vervet
   rt random-float 360        ;; random direction and random distance
   fd ((random step) + step)  ;;move a random distance between step and 2 steps
   ;predator-check             ;; check for predators REMOVE
end

to random-move-in-area                        ;;move randomly in area
  go-to-area item mypatchtype areaXY
end

to move-to-random-safearea                    ;; rule for moving randomly to a safe area
  go-to-area item (1 + random 3) areaXY       ;; go to randomly selected safe area
end

to move-to-closest-safearea                                  ;; rule for moving to closest safe area that is not vervet's current mypatchtype
  let bush_dist 100000                                       ;; large value, ensures vervet won't move to this patch type
  let tree_dist 100000
  let stone_dist 100000
  let bushXY item bushtype areaXY                            ;; get the coordinates for the areas 
  let treeXY item treetype areaXY 
  let stoneXY item stonetype areaXY
  if mypatchtype != bushtype                                 ;; reset distance values for eligible patch types 
    [set bush_dist distanceXY x-Cor bushXY y-Cor bushXY]
  if mypatchtype != treetype
    [set tree_dist distanceXY x-Cor treeXY y-Cor treeXY]
  if mypatchtype != stonetype
    [set stone_dist distanceXY x-Cor stoneXY y-Cor stoneXY]
  ifelse (tree_dist < stone_dist)                             ;; if trees closer than stones ...
    [ifelse (tree_dist < bush_dist)                           ;; if trees closer than bushes ...
      [go-to-area treeXY]                                     ;; trees closest, move to trees ...
      [go-to-area bushXY]]                                    ;; otherwise, bushes closest, move to bushes ...
    [ifelse (bush_dist < stone_dist)                          ;; otherwise, if bushes closer than stones ...
      [go-to-area bushXY]                                     ;; bushes closest, move to bushes ...
      [go-to-area stoneXY]                                    ;; otherwise, move to stone
    ]                                                                     
end

to go-to-area [area]                             ;; procedure to go to an area
  ask patch x-Cor area y-Cor area [              ;; get coordinates of area
  let apatch one-of patches at-points nearby     ;; get a patch in the area (?) 
     ;ask myself [move-to apatch color-anxiety]
  ask myself [move-to-patch apatch]              ;; move to the patch that was selected
  ]
  ;predator-check                                ;;move-to-patch calls predator check, redundant
end

to move-to-safearea                      ;; procedure for moving to safe area
  if make-move-decision = 1               ;; move to randomly selected safe area
     [move-to-random-safearea]
  if make-move-decision = 2               ;; move to closest mypatchtype area
    [move-to-closest-safearea]
end

to random-move-within                     ;;move a random distance within values set by user
  let step max-move - min-move
  rt random-float 360
  fd ((random step) + min-move)
end

to-report myhunger             ;; report hunger state of vervet
  if energy <= 2 [report 15]    ;; large hunger number; this ensures hunger overrides fear level
  report metabolism - energy   ;; hunger is the difference between metabolic need and energy
end

to-report myanxB
  report count mypredators                ;;reports number of predators within sightrad of vervet
end

to-report myanxB2                ;;reports number of predators weighted by distance
  let anxsum 0
  let dis 0
  let x xcor
  let y ycor
  ask leopardshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis]
  ask hawkshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis]
  ask snakeshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis]
  report anxsum * anxiety-const
end

to-report myanxB3                ;;reports number of predators weighted by square of distance
  let anxsum 0
  let dis 0
  let x xcor
  let y ycor
  ask leopardshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis ^ 2]
  ask hawkshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis ^ 2]
  ask snakeshere [
    set dis 1 / distancexy x y
    set anxsum anxsum + dis ^ 2]
  report anxsum * anxiety-const
end

to-report make-move-decision              ;; procedure to be used in future for decision making by vervet
  report 2                                ;; currently always returns 2; see above procedure
end

to determine-index
  determine-anx-index
  determine-hun-index
end

to determine-anx-index
  let x anx_cap / 3
  ifelse anx < x [set anx_index 0] [
   ifelse anx < (2 * x) [set anx_index 1]
   [set anx_index 2]
  ]
end

to determine-hun-index
  ifelse myhunger < 3 [set hun_index 0] [
    ifelse myhunger < 6 [set hun_index 1] [
      set hun_index 2
    ]
  ]
end

to-report mymove                                     ;;report 0 or 1 from matrix entry corresponding to indexes
  report item hun_index (item anx_index matrix)
end

to change-strategy-starve                            ;;adjust matrix by changing a 1 to a 0, start with highest hunger lowest anxiety, etc
  ifelse item 2 (item 0 matrix) = 1 [set matrix replace-item 0 matrix (replace-item 2 item 0 matrix 0)] [
    ifelse item 2 (item 1 matrix) = 1 [set matrix replace-item 1 matrix (replace-item 2 item 1 matrix 0)] [
      ifelse item 2 (item 2 matrix) = 1 [set matrix replace-item 2 matrix (replace-item 2 item 2 matrix 0)] [
        ifelse item 1 (item 0 matrix) = 1 [set matrix replace-item 0 matrix (replace-item 1 item 0 matrix 0)] [
          ifelse item 1 (item 1 matrix) = 1 [set matrix replace-item 1 matrix (replace-item 1 item 1 matrix 0)] [
            ifelse item 1 (item 2 matrix) = 1 [set matrix replace-item 2 matrix (replace-item 1 item 2 matrix 0)] [
              ifelse item 0 (item 0 matrix) = 1 [set matrix replace-item 0 matrix (replace-item 0 item 0 matrix 0)] [
                ifelse item 0 (item 1 matrix) = 1 [set matrix replace-item 1 matrix (replace-item 0 item 1 matrix 0)] [
                  ifelse item 0 (item 2 matrix) = 1 [set matrix replace-item 2 matrix (replace-item 0 item 2 matrix 0)] [
                    show matrix]
                  
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ]
end

to change-strategy-eaten
  ifelse item 0 (item 2 matrix) = 0 [set matrix replace-item 2 matrix (replace-item 0 item 2 matrix 1)] [
    ifelse item 1 (item 2 matrix) = 0 [set matrix replace-item 2 matrix (replace-item 1 item 2 matrix 1)] [
      ifelse item 2 (item 2 matrix) = 0 [set matrix replace-item 2 matrix (replace-item 2 item 2 matrix 1)] [
        ifelse item 0 (item 1 matrix) = 0 [set matrix replace-item 1 matrix (replace-item 0 item 1 matrix 1)] [
          ifelse item 1 (item 1 matrix) = 0 [set matrix replace-item 1 matrix (replace-item 1 item 1 matrix 1)] [
            ifelse item 2 (item 1 matrix) = 0 [set matrix replace-item 1 matrix (replace-item 2 item 1 matrix 1)] [
              ifelse item 0 (item 0 matrix) = 0 [set matrix replace-item 0 matrix (replace-item 0 item 0 matrix 1)] [
                ifelse item 1 (item 0 matrix) = 0 [set matrix replace-item 0 matrix (replace-item 1 item 0 matrix 1)] [
                  ifelse item 2 (item 0 matrix) = 0 [set matrix replace-item 0 matrix (replace-item 2 item 0 matrix 1)] [
                    show matrix
                  ]
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ]
end

to generate-random-matrix
  let x random 2
  set matrix replace-item 0 matrix (replace-item 0 item 0 matrix x)
  set x random 2
  set matrix replace-item 0 matrix (replace-item 1 item 0 matrix x)
  set x random 2
  set matrix replace-item 0 matrix (replace-item 2 item 0 matrix x)
  set x random 2
  set matrix replace-item 1 matrix (replace-item 0 item 1 matrix x)
  set x random 2
  set matrix replace-item 1 matrix (replace-item 1 item 1 matrix x)
  set x random 2
  set matrix replace-item 1 matrix (replace-item 2 item 1 matrix x)
  set x random 2
  set matrix replace-item 2 matrix (replace-item 0 item 2 matrix x)
  set x random 2
  set matrix replace-item 2 matrix (replace-item 1 item 2 matrix x)
  set x random 2
  set matrix replace-item 2 matrix (replace-item 2 item 2 matrix x)
end

to vector-move
  setxy xcor + vector-xsum ycor + vector-ysum
end

to-report vector-xsum                        ;;IMPORTANT angle measurements in netlogo are different: 12 o'clock = 0, increase in clockwise direction. Hence sin->xcoord, cos->ycoord
  let x xcor
  let y ycor
  let xcomp sum [sin (towards myself) * (sightrad - distancexy x y)] of mypredators
  report xcomp
end

to-report vector-ysum
  let x xcor
  let y ycor
  let ycomp sum [cos (towards myself) * (sightrad - distancexy x y)] of mypredators
  report ycomp
end


;;=========================PREDATOR PROCEDURES===================================

to predator-movement
  ask leopards                                               ;; move predators -- needs work
    [move-leopard]
  ask hawks
    [move-hawk]
  ask snakes
    [move-snake]
end

to move-leopard
  let fmates no-turtles                                     ;; initialize collection to be empty set; fmates = flock mates (of vervets)
  if ticks mod 2 = 0                                        ;; move every 4th tick
    [set fmates (find-vervets Leopard-vision) with [mypatchtype != treetype] ;; find how many vervets up to distance Leopard-vision, except those in trees
    if any? fmates [set heading newheading fmates]          ;; set heading towards the vervets
    fd 1]                                                   ;; move forward distance 1
  let prey one-of vervets-here
  if prey != nobody [ask prey [set myfear fear set anx fear set eaten eaten + 1 generate-random-matrix]]
end

to move-hawk
 let fmates no-turtles
 if ticks mod 1 = 0 
  [set fmates (find-vervets Eagle-vision) with [mypatchtype != bushtype]
  if any? fmates [set heading newheading fmates]
  fd 1]
  let prey one-of vervets-here
  if prey != nobody [ask prey [set myfear fear set anx fear set eaten eaten + 1 generate-random-matrix]]
end

to move-snake
 let fmates no-turtles
 if ticks mod 3 = 0 
   [set fmates (find-vervets 2) with [mypatchtype != stonetype]
   if any? fmates [set heading newheading fmates]
   fd 1]
  let prey one-of vervets-here
  if prey != nobody [ask prey [set myfear fear set anx fear set eaten eaten + 1 generate-random-matrix]]
end

to-report find-vervets [radius]  ;; find vervets within radius distance
  report vervets in-radius radius
end

to-report newheading [fmates]
  report atan mean [sin (towards myself + 180)] of fmates  ;; average of angular direction towards fmates set of turtle (bit of a kludge
                                                           ;; since it computes atan of mean sin/mean cos, not mean (atan of sin/cos))
              mean [cos (towards myself + 180)] of fmates
end

;----------------------procedures for decaying or increasing parameters-------
to decay-fear                                               ;;rule for decaying fear
  set myfear increment-parameter myfear (-1 * fear_decay)   ;; myfear -> myfear - fear_decay, fear-decay the amount by which fear decays
  ;if myfear < 0 [set myfear 0]                             ;; can't be negative
end

to decay-anx
  set anx increment-parameter anx (-1 * anxiety_decay)
end

to decay-anxiety                                            ;; rule for decaying anxiety and myanxiety
  change-anxiety mypatchtype (-1 * anxiety_decay) 
  change-myanxiety mypatchtype (-1 * anxiety_decay)
end

to decay-energy                                             ;;rule for decaying energy
  set energy increment-parameter energy (-1 * eDecay)
  ;if energy = 0 [die]
  ;if energy < 0 [set energy 0]
end

to eat-food                                                             ;; rule for energy gained by eating
  let foodunit 1
  if energy < metabolism
    [set energy increment-parameter energy foodunit                     ;; increase energy by foodunit
    ;ask patch-here [decrease-food foodunit]]
    ask patch-here [set food increment-parameter food (-1 * foodunit)]] ;; decay food parameter for the patch by foodunit
end

;to decrease-food [foodunit]
;  set food  food - foodunit
;end



 


;================================== event actions ========================
to color-anxiety                                                        ;;set the color  
                                                                        ;; the shade of the vervet based on its largest anxiety value and 
                                                                        ;; patchtype for that anxiety
  let thepatchtype position max-anxiety mytype_anxiety
  let colors [red green magenta cyan]
  ifelse AnxietyPlot
    [set color scale-color item thepatchtype colors max-anxiety 25 0]
    [set color scale-color item thepatchtype colors danger 50 0]
end

to-report max-anxiety
  report list-max mytype_anxiety
end

to-report mypatchtype
   report [patchtype] of patch-here
end

to-report checkforpredators1                            ;; procedure to check for predators (old procedure, no longer used)
;show mypredators
  ifelse any? mypredators with [any? hawks-here]        ;; are there any hawks here?...
  [record-patchtype patchtype hawkpred                  ;; if so, record patchtype and hawk
  color-patchtype set myfear fear report true]          ;;set fear, report patch and predator
    [ifelse any? mypredators  with [any? snakes-here]   
      [record-patchtype patchtype snakepred
      color-patchtype set myfear fear report true]
        [if any? mypredators with [any? leopards-here]
          [record-patchtype patchtype leopardpred
          color-patchtype set myfear fear report true]
        ]
     ]
  report false
end

to-report selectPredator     ;; procedure for vervet to select a predator that will NOT be searched for
  if mypatchtype = treetype [report hawkpred]
  if mypatchtype = bushtype [report leopardpred]
  ifelse mypatchtype = stonetype [report snakepred]
  [report 4]
  ;report random 3            ;; randomly select a predator  
end

to-report checkforpredators                      ;; procedure to check for predators
  ;let predator selectPredator                    ;; select a predator to be searched for UNNECESSARY AS HAWKSHERE,ECT OMIT PREDATOR
  let flag false
  if any? hawkshere                              ;; are there any hawks here? 
    [record-patchtype mypatchtype hawkpred       ;; if so, record patch type and hawk
     change-anxiety mypatchtype 1                ;; always do this, regardless of predator type; at the moment, change-anxiety and change-myanxiety change in // 12-10
     ;negative-learn-strategy                     ;; do negative learn for current strategy
     ;if predator != hawkpred or allPredators      ;; allPredators is set true or false by observer
     record-data mypatchtype                    ;; record data for the patchtype, activates change-myanxiety
     ;set myfear fear 
     set flag true]             ;; set fear, report patch and predator
  if any? snakeshere
    [record-patchtype mypatchtype snakepred
     change-anxiety mypatchtype 1 ;;always do this
     ;negative-learn-strategy
     ;if predator != snakepred or allPredators
     record-data mypatchtype
     ;set myfear fear 
     set flag true]
  if any? leopardshere
    [record-patchtype mypatchtype leopardpred
     change-anxiety mypatchtype 1 ;;always do this
     ;negative-learn-strategy
     ;if predator != leopardpred or allPredators
     record-data mypatchtype
     ;set myfear fear 
     set flag true]
  ;if flag = true [negative-learn-strategy]         ;;NOW WITHIN PREDATORCHECK
  report flag                                    ;; report true if a predator was found
end






to record-data [thepatchtype]              ;; procedure to record data
  negative-learn-patchtype thepatchtype    ;; always do this, but not used anywhere so far
  change-myanxiety thepatchtype 1          ;; update anxiety for the patch type
  ;negative-learn-strategy
end


to-report mypredators                                      ;; procedure to report the vervet's predators
  ;report neighbors
  report (turtle-set leopardshere hawkshere snakeshere)
end

to-report leopardshere                                        ;; report set of nearby leopards
  if mypatchtype != treetype [report (leopards in-radius sightrad)]  ;; except for treetype, report leopards up to distance 5  
  report no-turtles                                           ;; otherwise report no leopards
end
to-report hawkshere
  if mypatchtype != bushtype [report (hawks in-radius sightrad)]
  report no-turtles
end
to-report snakeshere
  if mypatchtype != stonetype [report (snakes in-radius sightrad)]
  report no-turtles
end

to record-patchtypeOLD [thepatchtype predtype]                  ;; old procedure, replaced by new version below
  ask self [set type_pred replace-item thepatchtype type_pred 
                                  ;(replace-item  predtype  (item thepatchtype type_pred) (item predtype (item thepatchtype type_pred) + 1)) ] 
                                  (replace-item  predtype  (item thepatchtype type_pred) increment-parameter (item predtype (item thepatchtype type_pred)) 1) ] 
  ask self [set type_prob replace-item thepatchtype type_prob negative-learn (item thepatchtype type_prob)
    set type_prob normalize-prob-list type_prob
    ]                                                           ;;update area learning probabilities
  ask self [set strat_prob replace-item mystrategy strat_prob negative-learn (item mystrategy strat_prob)
    set strat_prob normalize-prob-list-omit strat_prob 0        ;;make list into probabilities after it has been modified
  ]                                                             ;;update strategy learning probabilities
  ;ask self [set type_anxiety replace-item thepatchtype type_anxiety increment-parameter (item thepatchtype type_anxiety)] ;;update anxiety counts
  change-anxiety thepatchtype 1                                 ;;update anxiety
end

to record-patchtype [thepatchtype predtype]                        ;;record patchtype x predator type
  ask self [set type_pred replace-item thepatchtype type_pred 
      (replace-item  predtype  (item thepatchtype type_pred) increment-parameter (item predtype (item thepatchtype type_pred)) 1) ] 
end

to change-anxietyOLD [thepatchtype delta maxvalue]                  ;; old procedure
  let del1 delta
  let del2 delta
  if item thepatchtype type_anxiety + delta > maxvalue [set del1 (maxvalue - item thepatchtype type_anxiety)] ;set del1 to keep anxiety below its upper bound
  if myanxiety + delta > maxvalue [set del2 (maxvalue - myanxiety)] ;; set del2 to keep anxiety below its upper bound
  ask self [
    set type_anxiety replace-item thepatchtype type_anxiety increment-parameter (item thepatchtype type_anxiety) del1
    set myanxiety increment-parameter myanxiety del2
  ]
end

to change-anxiety [thepatchtype delta]                               ;; compute patch specific anxiety 
  ask self [
  set type_anxiety replace-item thepatchtype type_anxiety increment-parameter (item thepatchtype type_anxiety) delta ;; used for all predators
  set anxiety increment-parameter anxiety delta                      ;; increment anxiety
  ]
end

to change-myanxiety [thepatchtype delta]                              ;; compute anxiety of the vervet
  ask self [
    set mytype_anxiety replace-item thepatchtype mytype_anxiety increment-parameter (item thepatchtype mytype_anxiety) delta ;; used for what vervet sees
    set myanxiety increment-parameter myanxiety delta
  ]
end
to-report get-patch-predator [thepatchtype thepredatortype thelist]   ;; use to get a patch-predator value from a vervet monkey
   report (item thepredatortype (item thepatchtype thelist))
end

to color-patchtype
  ifelse patchtype = grasstype
    [color-grass-area]
    [ifelse patchtype = treetype
      [color-tree-area]
      [ifelse patchtype = stonetype
        [color-stone-area]
        [color-bush-area]
      ]
    ]
end


;;==================procedures for setting up landscape and populating with agents =====================================

to setup-area                                      ;; this determines an area that can be filled with an envionmental feature
                                                   ;; such as trees, bushes, rocks
  set nearby moore-offsets feature-radius true     ;;use a global variable to store the offsets list
                                                   ;; Now whenever a turtle or patch wants to refer
                                                   ;; to its neighborhood, it says "patches at-points nearby".
end

to landscape-location
  set grasstype 0                                  ;; mapping from resource type to index value
  set bushtype 1
  set stonetype 2
  set treetype 3
  set areaXY [[0 0] [25 15] [-10 -20] [-20 20 ]]   ;; coordinate location for center of grass, bush, stone tree  regions in that order
  set foodstock [2 0 0 0]                          ;; food stock in [grass, bush, stone, tree] areas
end

to setup-breeds
 setup-environment-objects
 setup-animal-objects
end

to create-landscape
  ;color-the-grass 
  make-grass
  make-bushes
  make-trees
  make-stones
end

to create-animals
  make-vervets
  make-leopards
  make-snakes
  make-hawks
end

to setup-environment-objects
  set-default-shape trees "tree"
  set-default-shape bushes "plant"
  set-default-shape stones "tile stones"
end

to setup-animal-objects
  set-default-shape vervets "person"
  set-default-shape snakes "caterpillar"
  set-default-shape leopards "cat"
  set-default-shape hawks "hawk"
end

;to color-the-grass
 ; ask patches [
  ;  set pcolor green + 4
  ;]
;end

;; ====================Procedures for making objects=====================================================


to growgrass  ;; only grow grass if there is no vervet on the patch
  ask self [if (food < 2) and (count vervets-here = 0 and ticks mod 900 = 0) [set food food + 1]]
end

to make-grass
  ask patches [set food item grasstype foodstock set pcolor green + 4]
end

to make-bushes
   ask patch x-Cor item bushtype areaXY y-Cor item bushtype areaXY [  ;; location of the bush area
 ;; ask n-of 1 patches [  ;; random location
      set-patchtype bushtype
      set food item bushtype foodstock
      ask n-of 50 patches at-points nearby [  ;; bushes located randomly in bush area
       sprout-bushes 1 [set size 2]  ;; set up bush area
    ]
  ]
end

to make-trees
  ask patch x-Cor item treetype areaXY y-Cor item treetype areaXY [
  ;;ask n-of 1 patches [  ;;use for a random located tree area
      set-patchtype treetype
      set food item treetype foodstock
      ask n-of 10 patches at-points nearby [
      sprout-trees 1 [set size 4] ;; set up grove of trees
    ]
  ]
end

to make-stones
   ask patch x-Cor item stonetype areaXY y-Cor item stonetype areaXY [
  ;;ask n-of 1 patches [  ;;use for a random located stone area
      set-patchtype stonetype
      set food item stonetype foodstock
      ask n-of 100 patches at-points nearby [
      sprout-stones 1 [set size 2] ;; set up open rock area
    ]
  ]
end

to set-patchtype [ptype]
  ask patches at-points nearby [set patchtype ptype set food item ptype foodstock]
end

to make-vervets
  create-vervets initial-vervets [
    setxy random-xcor random-ycor
    set color red
    set size 2
    set type_pred [[0 0 0] [0 0 0] [0 0 0] [0 0 0]]  ;; [patchtype:[predatortype] ... patchtype:[predator type]]
    set type_prob [0.5 0.5 0.5 0.5]; grass ....
    set strat_prob [0.0 0.33 0.33 0.33]; strategy 0, ...
    set energy metabolism 
    set type_anxiety [0 0 0 0]; predators that could possibly be seen by vervet
    set mytype_anxiety [0 0 0 0] ;predators seen by vervet
    set myfear 0
    set anxiety 0 ; anxiety based on predators that could be seen by vervet
    set myanxiety 0 ; anxiety based on predators seen by vervet
    set mystrategy 0
    set posct 0  ;keeps track of number of times predator-check is used
    set predct 0
    set negct 0  ;negative-learn used
    set strct 0  ;keeps track of number of times a strategy is selected and used
    set alert 0
    set thungera 0
    set thungerm 0
    set learnct 0
    set learncti 0
    set zeroct 0
    set alertct 0
    set negcta 0 
    set onect 0
    set twoct 0
    set threect 0
    set onenegct 0
    set twonegct 0
    set threenegct 0
    set eaten 0
    set anx 0
    set starve 0
    set patchcount [0 0 0 0]
    set matrix [[0 0 0] [1 1 1] [1 1 1]]
    set hun_index 0
    set anx_index 0
    set anx_cap 0
    ]
end

to make-snakes 
  create-snakes initial-snakes [
    find-new-spot stonetype
    set color blue
    set size 3
    ]
end


to make-leopards
  create-leopards initial-leopards [
    find-new-spot treetype
    ;set color yellow
    set size 2
    ]
end

to make-hawks
  create-hawks initial-hawks [
    find-new-spot bushtype
    set color gray
    set size 3
    ]
end

to find-new-spot [thePatchType]
  setxy random-xcor random-ycor
  ask patch-here [if patchtype = thePatchType
    [ask myself [find-new-spot thePatchType]]         ;; keep going until we find an unoccupied patch
  ]
end

;;  procedures for coloring areas ===========================

to color-environment
  ask patches [
   ifelse patchtype = grasstype [ color-grass-area growgrass] ;; shades of green for amount of grass
   [color-patchtype]                                          ;; set current color based on number of predator encounters in a patch type
  ]
end

to color-grass-area  ;; patch procedure
;  let num sumgrass
;  if num > 120 [set num 120]
;  if num < 15 [set num 15]
  ;set pcolor scale-color green num 150 0
  set pcolor scale-color green (food + 1)  (2 * item grasstype foodstock) 0
end

to color-tree-area  ;; patch procedure
  set pcolor scale-color blue sumtree 100 0
end

to color-bush-area  ;; patch procedure
  set pcolor scale-color yellow sumbush 100 0
end

to color-stone-area  ;; patch procedure
  set pcolor scale-color red sumstone 100 0
end

to eat  ;; turtle procedure

end

;; utilities ======================================================================

to-report list-max [thelist]
  report last sort thelist
end

to-report normalize-prob-list [prob_list]   
  let n -1
  let thelist prob_list
  foreach prob_list [set n n + 1 set prob_list replace-item n prob_list (normalize-prob ? thelist)]
  report prob_list
end

to-report normalize-prob-list-omit1 [prob_list omit deltaprob]
  let n -1
  ;;let thelist remove-item omit prob_list
  foreach prob_list [set n n + 1 if (n != omit and n != mystrategy)  [set prob_list replace-item n prob_list (modify-prob ? deltaprob)]]
  set n -1
  let thelist remove-item omit prob_list
  foreach prob_list [set n n + 1 if n != omit [set prob_list replace-item n prob_list (normalize-prob ? thelist)]]
  report prob_list  
end 

to-report normalize-prob-list-omit [prob_list omit]
  let n -1
  let thelist remove-item omit prob_list
  ;;foreach prob_list [set n n + 1 if (n != omit & n != mystrategy)  [set prob_list replace-item n prob_list (modify-prob ? deltaprob)]]
  foreach prob_list [set n n + 1 if n != omit [set prob_list replace-item n prob_list (normalize-prob ? thelist)]]
  report prob_list  
end 

to-report normalize-prob [prob prob_list]  ;;converts a relative probability into an absolute probability
  report (prob / sum prob_list)
end

to-report modify-prob [prob deltaprob]  ;;converts a relative probability into an absolute probability
  ifelse (prob + deltaprob) > 0 [report (prob + deltaprob)]
  [report 0]
end

to-report increment-parameter [parm_value delta]
  if (parm_value + delta) < 0 [report 0]
  report (parm_value + delta)
end

to-report x-Cor [XY]
  report item 0 XY
end

to-report y-Cor [XY]
  report item 1 XY
end

to-report moore-offsets [n include-center?]  ;;generate list of offsets
 let dim n * 2 + 1
 let result n-values (dim ^ 2)
              [list (? mod dim - n)
                    (floor (? / dim) - n)]
 ifelse include-center?
   [ report result ]
   [ report remove [0 0] result ]
end

to do-plotting
  if (ticks mod 10 = 0) [
;  set-current-plot "Probabilities"
  
;  if 1 = 2 [set-current-plot-pen "bush"
;  plot bushprob
;  set-current-plot-pen "tree"
;  plot treeprob
;  set-current-plot-pen "stone"
;  plot stoneprob
;  set-current-plot-pen "grass"
;  plot grassprob]
  
;  set-current-plot-pen "strategy 1"
;  plot strat1prob
;  set-current-plot-pen "strategy 2"
;  plot strat2prob
;  set-current-plot-pen "strategy 3"
;  plot strat3prob
;  if ticks > 300  ;;first ticks lead to high anxiety rate
;  [set-current-plot "Anxiety Rate"
  
;  ifelse AnxietyPlot [
;  set-current-plot-pen "anxiety"
;  plot 100 * mean_anxiety
;  set-current-plot-pen "vervet anxiety"
;  plot 300 * mean_myanxiety
;  set-current-plot-pen "area anxiety"
;  plot 100 * mean_type_anxiety 
;  set-current-plot-pen "vervet area anxiety"
;  plot 300 * mean_mytype_anxiety]
  
;  [set-current-plot-pen "danger"
;  plot 300 * danger]
;  ]
set-current-plot "Emotions"
set-current-plot-pen "anxiety"
plot mean_anx
;set-current-plot-pen "fear"
;plot mean_fear
set-current-plot-pen "hunger"
plot mean_hunger
;set-current-plot-pen "eaten"
;plot mean_eaten

set-current-plot "Anxiety Distribution"
let maxanx max [anx] of vervets
set-plot-x-range 0 maxanx + 1
histogram [anx] of vervets
  ]
end




;;==================flocking======================
;; modified from netlogo flocking model
;turtles-own [
;  flockmates         ;; agentset of nearby turtles
;  nearest-neighbor   ;; closest one of our flockmates
;]

;to setup
;  clear-all
;  crt population
;    [ set color yellow - 2 + random 7  ;; random shades look nice
;      set size 1.5  ;; easier to see
;      setxy random-xcor random-ycor ]
;end

;to go
  ;ask turtles [ flock ]
  ;; the following line is used to make the turtles
  ;; animate more smoothly.
  ;;repeat 5 [ ask turtles [ fd 0.2 ] display ]
  ;; for greater efficiency, at the expense of smooth
  ;; animation, substitute the following line instead:
   ;  ask turtles [ fd 1 ]
  ;tick
;end

to flock-movement [pdistance] ;; turtle procedure
  fd pdistance
  find-flockmates
  if any? flockmates
    [ find-nearest-neighbor
      ifelse distance nearest-neighbor < minimum-separation
        [ separate ]
        [ align
          cohere ] ]
end

to find-flockmates  ;; turtle procedure
  set flockmates other vervets in-radius vision
end

to find-nearest-neighbor ;; turtle procedure
  set nearest-neighbor min-one-of flockmates [distance myself]
end

;;; SEPARATE

to separate  ;; turtle procedure
  turn-away ([heading] of nearest-neighbor) max-separate-turn
end

;;; ALIGN

to align  ;; turtle procedure
  turn-towards average-flockmate-heading max-align-turn
end

to-report average-flockmate-heading  ;; turtle procedure
  ;; We can't just average the heading variables here.
  ;; For example, the average of 1 and 359 should be 0,
  ;; not 180.  So we have to use trigonometry.
  ;; Theoretically this could fail if both sums are 0
  ;; since atan 0 0 is undefined, but in practice that's
  ;; vanishingly unlikely.
  report atan sum [sin heading] of flockmates
              sum [cos heading] of flockmates
end

;;; COHERE

to cohere  ;; turtle procedure
  turn-towards average-heading-towards-flockmates max-cohere-turn
end

to-report average-heading-towards-flockmates  ;; turtle procedure
  ;; "towards myself" gives us the heading from the other turtle
  ;; to me, but we want the heading from me to the other turtle,
  ;; so we add 180
  report atan mean [sin (towards myself + 180)] of flockmates
              mean [cos (towards myself + 180)] of flockmates
end

;;; HELPER PROCEDURES

to turn-towards [new-heading max-turn]  ;; turtle procedure
  turn-at-most (subtract-headings new-heading heading) max-turn
end

to turn-away [new-heading max-turn]  ;; turtle procedure
  turn-at-most (subtract-headings heading new-heading) max-turn
end

;; turn right by "turn" degrees (or left if "turn" is negative),
;; but never turn more than "max-turn" degrees
to turn-at-most [turn max-turn]  ;; turtle procedure
  ifelse abs turn > max-turn
    [ ifelse turn > 0
        [ rt max-turn ]
        [ lt max-turn ] ]
    [ rt turn ]
end


;;================DATA COLLECTION & OUTPUT============================================

to set-global-counters
  set tfeara 0
  set tavoid 0
  set avgalerted 0
  set numstr1 0
  set numstr2 0
  set numstr3 0
  set str1sxs 0
  set str2sxs 0
  set str3sxs 0
end

to update-variables
  set Numvervets count vervets                                                ;;placed vervet counting within update variable block
  if Numvervets = 0 [stop]
  set sumgrass 0 set sumstone 0 set sumtree 0 set sumbush 0                                      ;; reset to 0, don't want cumulative sum
  set sumhawk 0 set sumsnake 0 set sumleopard 0
  foreach ([type_pred] of vervets) [foreach (item grasstype ?) [set sumgrass sumgrass + ?]]      ;; total number of encounters in grass area
                                      
  foreach ([type_pred] of vervets) [foreach (item stonetype ?) [set sumstone sumstone + ?]]
  foreach ([type_pred] of vervets) [foreach (item treetype ?) [set sumtree sumtree + ?]]
  foreach ([type_pred] of vervets) [foreach (item bushtype ?) [set sumbush sumbush + ?]]
  foreach ([type_pred] of vervets) [foreach (?) [set sumsnake sumsnake + (item snakepred ?)]]    ;; total number of encounters with snakes
  foreach ([type_pred] of vervets) [foreach (?) [set sumhawk sumhawk + (item hawkpred ?)]]
  foreach ([type_pred] of vervets) [foreach (?) [set sumleopard sumleopard + (item leopardpred ?)]]
  set strat1prob mean [item 1 strat_prob] of vervets                         ;; strategy 1: mean probability of doing strategy 1
  set strat2prob mean [item 2 strat_prob] of vervets
  set strat3prob mean [item 3 strat_prob] of vervets
  set grassprob mean [item grasstype type_prob] of vervets                   ;; current mean probability of going to grass area
  set bushprob mean [item bushtype type_prob] of vervets
  set stoneprob mean [item stonetype type_prob] of vervets
  set treeprob mean [item treetype type_prob] of vervets
  set mean_mytype_anxiety mean [item mypatchtype mytype_anxiety] of vervets  ;; mean patch anxiety based on vervet encounters
  set mean_type_anxiety mean [item mypatchtype type_anxiety] of vervets      ;; mean patch anxiety based on all possible encounters
  set mean_anxiety mean [anxiety] of vervets                                 ;; mean anxiety based on all possible predator encounters regardless of patch 
  set mean_myanxiety mean [myanxiety] of vervets                             ;; mean anxiety of vervets based on actual encoungters regardless of patch
  set danger (mean_anxiety - mean_myanxiety)                                 ;; ??? difference between anxiety based on all possible predators and anxiety based on actual predator encounters
 ; ask vervets [update-fear]
 ; ask vervets [if max-anxiety > 10 [show (word type_anxiety1 "  " type_anxiety "  " type_pred)]]
 let x sum [alertct] of vervets
 set avgalerted x / numvervets
 
 set mean_fear mean [myfear] of vervets                        ;;new plot
 set mean_anx mean [anx] of vervets
 set mean_hunger mean [myhunger] of vervets
 set mean_eaten mean [eaten] of vervets
end

to update-statistics
  if (obtain-data-increment != 0) and (ticks mod obtain-data-increment = 0) [
    calcfitness1
    calcfitness2
    calcfitness3
  ]
end

to calcfitness1
  let x 0
  let y 0
  let z 0
  let alpha 0
  let beta 0
  let delta 0
  let gamma 0
  let epsilon 0
  let omega 0
  type "--------------------------------------------------------------Tick: " print ticks
  ask vervets [
   if item 1 strat_prob > item 2 strat_prob and item 1 strat_prob > item 3 strat_prob [
     set x x + 1
     set y y + calc-idle                              ;;reports total idle moves while outputing # to control panel
     set z z + calc-eat            ;;total moves eating grass
     set alpha alpha + calc-pred           ;;total predator checks
     set beta beta + calc-see          ;;total predator checks that sight predators
     set delta delta + calc-str         ;;total strategy moves/fear-moves
     set gamma gamma + calc-esc         ;;total strategy moves ending in positive learning/escaping from predators
     set epsilon epsilon + calc-str-1      ;;strategy moves with leading strategy
     set omega omega + calc-esc-1      ;;successful strategy moves with leading strategy 
  ]]
  set numstr1 x
  if epsilon != 0 [set str1sxs omega / epsilon]
  type "Total 1: " print x 
  if x != 0 [
  type "Idle avg: " type y / x type " Eat avg: " print z / x 
  type "Avg Predchecks: " type alpha / x type " Avg Strmoves: " print delta / x
  if alpha != 0 and delta != 0 [type "Pred spot: " type 100 * beta / alpha type "%" type " Escaped: " type 100 * gamma / delta print "%"]
  if epsilon != 0 [type "Str success: " type 100 * omega / epsilon print "%"]
  ]
  print " " print " "
end

to calcfitness2
  let x 0
  let y 0
  let z 0
  let alpha 0
  let beta 0
  let delta 0
  let gamma 0
  let epsilon 0
  let omega 0
  ask vervets [
   if item 2 strat_prob > item 1 strat_prob and item 2 strat_prob > item 3 strat_prob [
     set x x + 1
     set y y + calc-idle                              ;;reports total idle moves while outputing # to control panel
     set z z + calc-eat            ;;total moves eating grass
     set alpha alpha + calc-pred           ;;total predator checks
     set beta beta + calc-see          ;;total predator checks that sight predators
     set delta delta + calc-str         ;;total strategy moves/fear-moves
     set gamma gamma + calc-esc         ;;total strategy moves ending in positive learning/escaping from predators
     set epsilon epsilon + calc-str-2      ;;strategy moves with leading strategy
     set omega omega + calc-esc-2      ;;successful strategy moves with leading strategy 
  ]]
  set numstr2 x
  if epsilon != 0 [set str2sxs omega / epsilon]
  type "Total 2: " print x 
  if x != 0 [
  type "Idle avg: " type y / x type " Eat avg: " print z / x 
  type "Avg Predchecks: " type alpha / x type " Avg Strmoves: " print delta / x
  if alpha != 0 and delta != 0 [type "Pred spot: " type 100 * beta / alpha type "%" type " Escaped: " type 100 * gamma / delta print "%"]
  if epsilon != 0 [type "Str success: " type 100 * omega / epsilon print "%"]
  ]
  print " " print " "
end

to calcfitness3
  let x 0
  let y 0
  let z 0
  let alpha 0
  let beta 0
  let delta 0
  let gamma 0
  let epsilon 0
  let omega 0
  ask vervets [
   if item 3 strat_prob > item 2 strat_prob and item 3 strat_prob > item 1 strat_prob [
     set x x + 1
     set y y + calc-idle                              ;;reports total idle moves while outputing # to control panel
     set z z + calc-eat            ;;total moves eating grass
     set alpha alpha + calc-pred           ;;total predator checks
     set beta beta + calc-see          ;;total predator checks that sight predators
     set delta delta + calc-str         ;;total strategy moves/fear-moves
     set gamma gamma + calc-esc         ;;total strategy moves ending in positive learning/escaping from predators
     set epsilon epsilon + calc-str-3      ;;strategy moves with leading strategy
     set omega omega + calc-esc-3      ;;successful strategy moves with leading strategy 
  ]]
  set numstr3 x
  if epsilon != 0 [set str3sxs omega / epsilon]
  type "Total 3: " print x 
  if x != 0 [
  type "Idle avg: " type y / x type " Eat avg: " print z / x 
  type "Avg Predchecks: " type alpha / x type " Avg Strmoves: " print delta / x
  if alpha != 0 and delta != 0 [type "Pred spot: " type 100 * beta / alpha type "%" type " Escaped: " type 100 * gamma / delta print "%"]
  if epsilon != 0 [type "Str success: " type 100 * omega / epsilon print "%"]
  ]
  print " " print " "
end

;;----------------------------------------------------vervet fitness variable counting procedures

to-report calc-idle
  let x learncti
  if indiv-vervet-data = true [type "Idle: " show x]
  report x
end

to-report calc-eat
  let x thungera - thungerm
  if indiv-vervet-data = true [type "Eat: " show x]
  report x
end

to-report calc-pred
  let x posct
  if indiv-vervet-data = true [type "Predchecks: " show x]
  report x
end

to-report calc-see
  let x predct
  if indiv-vervet-data = true [type "Preds spotted: " show x]
  report x
end

to-report calc-str
  let x strct
  if indiv-vervet-data = true [type "Strmoves: " show x]
  report x
end

to-report calc-esc
  let x learnct
  if indiv-vervet-data = true [type "Successful moves: " show x]
  report x
end

to-report calc-str-1
  let x onect
  if indiv-vervet-data = true [type "Leading strmoves: " show x]
  report x
end

to-report calc-esc-1
  let x onect - onenegct
  if indiv-vervet-data = true [type "Leading sucsfulmoves: " show x]
  report x
end

to-report calc-str-2
  let x twoct
  if indiv-vervet-data = true [type "Leading strmoves: " show x]
  report x
end

to-report calc-esc-2
  let x twoct - twonegct
  if indiv-vervet-data = true [type "Leading sucsfulmoves: " show x]
  report x
end

to-report calc-str-3
  let x threect
  if indiv-vervet-data = true [type "Leading strmoves: " show x]
  report x
end

to-report calc-esc-3
  let x threect - threenegct
  if indiv-vervet-data = true [type "Leading sucsfulmoves: " show x]
  report x
end

;;===================GLOBAL VARS=====================================================

to set-globals
  set fear 10                                      ;; fear value for predator encounter
  set metabolism 8                                 ;; Note: lose 1 unit of energy per hour
                                                   ;; avoid initializing all turtles, which is a bit slow; all variables are initially set to zero

  set leopardpred 0                                ;; mapping from animal type to index value
  set hawkpred 1
  set snakepred 2
  set danger 0
  
end




; *** IDP in Human Complex Systems Copyright Notice ***
;
; This model was created as part of the project: Workshop On Vervet Communication
; IDP in Human Complex Systems, UCLA
@#$#@#$#@
GRAPHICS-WINDOW
366
10
1206
911
41
43
10.0
1
20
1
1
1
0
1
1
1
-41
41
-43
43
1
1
1
ticks
30.0

BUTTON
79
15
134
48
go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
19
14
74
47
setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
13
83
129
116
initial-leopards
initial-leopards
0
40
10
1
1
NIL
HORIZONTAL

SLIDER
14
52
125
85
initial-vervets
initial-vervets
0
100
25
1
1
NIL
HORIZONTAL

SLIDER
130
51
229
84
initial-snakes
initial-snakes
0
10
5
1
1
NIL
HORIZONTAL

SLIDER
129
83
229
116
initial-hawks
initial-hawks
0
20
5
1
1
NIL
HORIZONTAL

SLIDER
10
114
127
147
feature-radius
feature-radius
0
20
10
1
1
NIL
HORIZONTAL

SLIDER
128
114
220
147
b
b
0
1
0.5
0.1
1
NIL
HORIZONTAL

SLIDER
127
147
224
180
fear_decay
fear_decay
0
1
0.2
.1
1
NIL
HORIZONTAL

SLIDER
10
146
127
179
anxiety_decay
anxiety_decay
0
.5
0.1
.01
1
NIL
HORIZONTAL

PLOT
8
191
274
311
Emotions
time
anxiety
0.0
10.0
0.0
1.0
true
true
"" ""
PENS
"anxiety" 1.0 0 -16777216 true "" ""
"hunger" 1.0 0 -13345367 true "" ""
"fear" 1.0 0 -10899396 true "" ""
"eaten" 1.0 0 -1184463 true "" ""

SLIDER
151
713
353
746
vision
vision
0
10
0
0.5
1
patches
HORIZONTAL

SLIDER
151
844
354
877
max-separate-turn
max-separate-turn
0
20
1.5
0.25
1
degrees
HORIZONTAL

SLIDER
151
779
354
812
max-align-turn
max-align-turn
0
20
5.25
.25
1
degrees
HORIZONTAL

SLIDER
151
812
356
845
max-cohere-turn
max-cohere-turn
0
20
3
.25
1
degrees
HORIZONTAL

SLIDER
151
746
356
779
minimum-separation
minimum-separation
0
5
0
.25
1
patches
HORIZONTAL

SWITCH
135
15
225
48
Flock
Flock
1
1
-1000

SLIDER
226
147
318
180
eDecay
eDecay
0
1
0.2
.05
1
NIL
HORIZONTAL

SWITCH
227
14
340
47
allPredators
allPredators
1
1
-1000

SWITCH
229
49
337
82
AnxietyPlot
AnxietyPlot
0
1
-1000

SLIDER
182
648
354
681
Leopard-Vision
Leopard-Vision
0
20
9
1
1
NIL
HORIZONTAL

SLIDER
182
680
354
713
Eagle-vision
Eagle-vision
0
30
13
1
1
NIL
HORIZONTAL

SWITCH
7
876
152
909
indiv-vervet-data
indiv-vervet-data
0
1
-1000

SLIDER
160
877
351
910
obtain-data-increment
obtain-data-increment
0
100
0
1
1
ticks
HORIZONTAL

SLIDER
229
82
337
115
sightrad
sightrad
0
40
20
1
1
NIL
HORIZONTAL

PLOT
8
317
322
486
Anxiety Distribution
anxiety level
number vervets
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 1 -16777216 true "" ""

SLIDER
220
114
337
147
a
a
0
1
0.2
.01
1
NIL
HORIZONTAL

MONITOR
7
832
64
877
Eaten
sum [eaten] of vervets
0
1
11

MONITOR
7
788
66
833
Starved
sum [starve] of vervets
0
1
11

SLIDER
182
616
354
649
max-move
max-move
0
50
15
1
1
NIL
HORIZONTAL

SLIDER
182
583
354
616
min-move
min-move
0
50
10
1
1
NIL
HORIZONTAL

SLIDER
182
551
354
584
anxiety-const
anxiety-const
0
30
20
1
1
NIL
HORIZONTAL

SLIDER
259
518
354
551
anxiety-type
anxiety-type
1
3
1
1
1
NIL
HORIZONTAL

MONITOR
70
743
133
788
Avg Grass
mean [item 0 patchcount] of vervets
17
1
11

MONITOR
70
787
131
832
Avg Bush
mean [item bushtype patchcount] of vervets
17
1
11

MONITOR
70
832
133
877
Avg Stone
mean [item stonetype patchcount] of vervets
17
1
11

MONITOR
7
743
65
788
Avg Tree
mean [item treetype patchcount] of vervets
17
1
11

MONITOR
3
559
53
604
NIL
matrix00
17
1
11

MONITOR
53
559
103
604
NIL
matrix01
17
1
11

MONITOR
103
559
153
604
NIL
matrix02
17
1
11

MONITOR
3
604
53
649
NIL
matrix10
17
1
11

MONITOR
53
604
103
649
NIL
matrix11
17
1
11

MONITOR
103
604
153
649
NIL
matrix12
17
1
11

MONITOR
3
648
53
693
NIL
matrix20
17
1
11

MONITOR
53
648
103
693
NIL
matrix21
17
1
11

MONITOR
103
649
153
694
NIL
matrix22
17
1
11

@#$#@#$#@
## WHAT IS IT?

This model was created by Prof Dwight Read (UCLA Anthropology) and Prof Francis Steen (UCLA Communications Studies) of UCLA's Interdepartmental Program in Human Complex Systems, Starting in Winter 2011, Philip Bonushkin participated in the development. In the spring of 2010, Andy Olson, an undergraduate in the Program, contributed documentation. The purpose of the model is to explore the evolution of representational communication, based on the documented behavior of vervets in the wild (Seyfarth, Cheney, & Marler, 1980). Vervets us distinct alarm calls for three types of predators: leopards, snakes, and hawks. While there is no location in the vervets' habitat where they can seek effective shelter from all three predator types, they seek out bushes to conceal themselves from hawks, trees to escape from leopards, and stoney ground to stay safe from snakes. The vervet model is incomplete. See Version Information below for the introduction of major features.
   
## VERSION INFORMAITON

2011-03-01: Vervets 9.3.2 adds alert, alertrad, and alertct. When a vervet spots predators its alert variable is switched from 0 to 1. Any vervets with alerted vervets within radius alertrad act as though they've seen a predator. Alert is switched back to 0 immediately after escaping predators. Also, vervets  only check for alerted vervets after checking for predators.  
2011-02-22: Vervets 9.3.1 for Netlogo 4.1.2 replaces strategy 3 with new strategy: vervets are transported to the safe-area specific to the predator they encounter. 2011-02-17: Vervets 9.3.0 for NetLogo 4.1.2 completes the modifications to the core learning algorithm. Contributed by Philip Bonushkin. 2011-01-28: Vervets 9.2.3 for NetLogo 4.1.2 modifies the core learning algorithm by redistributing the probability of a particular strategy on positive and negative learning events. Contributed by Philip Bonushkin. 2011-01-28: Vervets 9.2.2 for NetLogo 4.1.2 adds counters for strategy, positive learn, and negative learn as a means to diagnose the vervets' excessive commitment to a particular strategy. Contributed by Philip Bonushkin. 2010-06-20: In this version of the model, Vervets 9.2.1 for NetLogo 4.1.0, the vervets get stuck on a particular strategy. This problem is solved in 9.2.3.
   
## HOW IT WORKS

The simulation begins with setting up the world. Many variables can be set, including food, fear, area, metabolism, number and vision of predators, and more. On each iteration, vervet energy decays based on their metabolism. The 3 predator types also move. Leopards move based on where they see vervets (except in trees). Hawks and snakes move with special consideration for bushes and stones, respectively. Vervets behavior is regulated by emotion. The model implements anxiety as a lossy mechanism for aggregating predator encounters, without the need for an infinite memory stack. Fear is a measure of the number of predators seen by the vervet. Hunger is the inverse of metabolic reserve. Vervet action is based on whether or not their fear exceeds their hunger. If it does, they will act out of fear (for safety). If not, they will act to satisfy hunger, even if they are afraid. Vervets experience both positive and negative learning. The strategies are selected using a random number from 0 to 1; this and the strategy's respective probabilities dictate which strategy is used at each strategy move. Vervet color changes based on anxiety. They report when they see a predator, and whether the patch they occupy has food. The color of a particular patch within the safe areas is determined by the number of predator encounters there; the shade of green outside the safe areas indicates the availability of food. The vervets can optionally display flocking behavior based on the proximity of others.
   
## HOW TO USE IT

SETUP: sets the initial model GO: starts and stops simulation FLOCK: turns off and on flocking behavior allPREDATORS: turns on/off use of all predators INITIAL: sets initial number of agents (vervets, snakes, hawks, leopards depending on button) ANXIETY PLOT: toggles graph of vervet anxiety FEATURE RADIUS: sets radius of features, i.e. tree or bush ANXIETY/FEAR DECAY: adjusts how fast anxiety and fear decrease in vervets eDECAY: rate of energy decrease in vervets LEOPARD/EAGLE VISION: sets distance leopards and eagles (respectively) can see VISION: sets vervet vision (used in flocking etc) MINIMUM SEPARATION: sets minimum distance between vervets MAX ALIGN/COHERE/SEPARATE TURN: defines agents headings while aligning/cohering/separating
   
## THINGS TO NOTICE

Run default settings. Which population grows -- predators or vervets? Which predator is most successful? Is any equilibrium reached?
   
## THINGS TO TRY

Turn on flocking and run the simulation. How does this change the model? Adjust the number of vervets initially alive. How does this change the system? Adjust the number of various predators present. How do different predator mixes affect the vervets? Adjust the rate at which vervets lose anxiety and fear. What change does this cause in vervets, if any? Does changing the metabolic rate of vervets change their actions or population at all? Change the vision of the leopards and/or hawks. What is the effect? What settings are best for the vervets? What settings benefit each predator type the most?
   
## EXTENDING THE MODEL

This model explores how the vervets act and communicate under the threat of these three predators. How can it be extended to add further factors? What could we add to the environment to add another variable that affects the vervets� actions? What inter-vervet behavior besides flocking might we add? What if we let the predators learn from their encounters? What might the effects be?
   
## CREDITS AND REFERENCES

To refer to this model in any written materials: Read, Dwight and Francis Steen (2008): "Reducing Uncertainty in Costly Information Gathering: An Agent-Based Model of Vervet Monkey Warning Cries", a simulation created in the UCLA Human Complex Systems Program. "Monkey Responses to Three Different Alarm Calls: Evidence of Predator Classification and Semantic Communication" Robert M. Seyfarth; Dorothy L. Cheney; Peter Marler Science, New Series, Vol. 210, No. 4471. (Nov. 14, 1980), pp. 801-803. Stable URL: http://links.jstor.org/sici?sici=0036-8075%2819801114%293%3A210%3A4471%3C801%3AMRTTDA%3E2.0.CO%3B2-N "Meaning and Mind in Monkeys" Robert M. Seyfarth and Dorothy L. Cheney Scientific American, December 1992, 122-128
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

cat
false
0
Line -7500403 true 285 240 210 240
Line -7500403 true 195 300 165 255
Line -7500403 true 15 240 90 240
Line -7500403 true 285 285 195 240
Line -7500403 true 105 300 135 255
Line -16777216 false 150 270 150 285
Line -16777216 false 15 75 15 120
Polygon -955883 true false 300 15 285 30 255 30 225 75 195 60 255 15
Polygon -1184463 true false 285 135 210 135 180 150 180 45 285 90
Polygon -955883 true false 120 45 120 210 180 210 180 45
Polygon -1184463 true false 180 195 165 300 240 285 255 225 285 195
Polygon -955883 true false 180 225 195 285 165 300 150 300 150 255 165 225
Polygon -1184463 true false 195 195 195 165 225 150 255 135 285 135 285 195
Polygon -1184463 true false 15 135 90 135 120 150 120 45 15 90
Polygon -1184463 true false 120 195 135 300 60 285 45 225 15 195
Polygon -955883 true false 120 225 105 285 135 300 150 300 150 255 135 225
Polygon -1184463 true false 105 195 105 165 75 150 45 135 15 135 15 195
Polygon -1184463 true false 285 120 270 90 285 15 300 15
Line -7500403 true 15 285 105 240
Polygon -1184463 true false 15 120 30 90 15 15 0 15
Polygon -955883 true false 0 15 15 30 45 30 75 75 105 60 45 15
Line -16777216 false 164 262 209 262
Line -16777216 false 223 231 208 261
Line -16777216 false 136 262 91 262
Line -16777216 false 77 231 92 261

caterpillar
true
0
Polygon -7500403 true true 165 210 165 225 135 255 105 270 90 270 75 255 75 240 90 210 120 195 135 165 165 135 165 105 150 75 150 60 135 60 120 45 120 30 135 15 150 15 180 30 180 45 195 45 210 60 225 105 225 135 210 150 210 165 195 195 180 210
Line -16777216 false 135 255 90 210
Line -16777216 false 165 225 120 195
Line -16777216 false 135 165 180 210
Line -16777216 false 150 150 201 186
Line -16777216 false 165 135 210 150
Line -16777216 false 165 120 225 120
Line -16777216 false 165 106 221 90
Line -16777216 false 157 91 210 60
Line -16777216 false 150 60 180 45
Line -16777216 false 120 30 96 26
Line -16777216 false 124 0 135 15

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

hawk
true
0
Polygon -7500403 true true 151 170 136 170 123 229 143 244 156 244 179 229 166 170
Polygon -16777216 true false 152 154 137 154 125 213 140 229 159 229 179 214 167 154
Polygon -7500403 true true 151 140 136 140 126 202 139 214 159 214 176 200 166 140
Polygon -16777216 true false 151 125 134 124 128 188 140 198 161 197 174 188 166 125
Polygon -7500403 true true 152 86 227 72 286 97 272 101 294 117 276 118 287 131 270 131 278 141 264 138 267 145 228 150 153 147
Polygon -7500403 true true 160 74 159 61 149 54 130 53 139 62 133 81 127 113 129 149 134 177 150 206 168 179 172 147 169 111
Circle -16777216 true false 144 55 7
Polygon -16777216 true false 129 53 135 58 139 54
Polygon -7500403 true true 148 86 73 72 14 97 28 101 6 117 24 118 13 131 30 131 22 141 36 138 33 145 72 150 147 147

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

link
true
0
Line -7500403 true 150 0 150 300

link direction
true
0
Line -7500403 true 150 150 30 225
Line -7500403 true 150 150 270 225

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -10899396 true false 135 90 165 300
Polygon -13840069 true false 135 255 90 210 45 195 75 255 135 285
Polygon -13840069 true false 165 255 210 210 255 195 225 255 165 285
Polygon -1184463 true false 135 180 90 135 45 120 75 180 135 210
Polygon -13840069 true false 165 180 165 210 225 180 255 120 210 135
Polygon -13840069 true false 135 105 90 60 45 45 75 105 135 135
Polygon -13840069 true false 165 105 165 135 225 105 255 45 210 60
Polygon -13840069 true false 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tile stones
false
0
Polygon -955883 true false 0 240 45 195 75 180 90 165 90 135 45 120 0 135
Polygon -6459832 true false 300 240 285 210 270 180 270 150 300 135 300 225
Polygon -6459832 true false 225 300 240 270 270 255 285 255 300 285 300 300
Polygon -955883 true false 0 285 30 300 0 300
Polygon -955883 true false 225 0 210 15 210 30 255 60 285 45 300 30 300 0
Polygon -955883 true false 0 30 30 0 0 0
Polygon -6459832 true false 15 30 75 0 180 0 195 30 225 60 210 90 135 60 45 60
Polygon -6459832 true false 0 105 30 105 75 120 105 105 90 75 45 75 0 60
Polygon -6459832 true false 300 60 240 75 255 105 285 120 300 105
Polygon -6459832 true false 120 75 120 105 105 135 105 165 165 150 240 150 255 135 240 105 210 105 180 90 150 75
Polygon -955883 true false 90 300 150 285 210 300
Polygon -6459832 true false 30 285 75 285 120 270 150 270 150 210 90 195 60 210 15 255
Polygon -955883 true false 180 285 240 255 255 225 255 195 240 165 195 165 150 165 135 195 165 210 165 255

tree
false
0
Circle -10899396 true false 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -10899396 true false 50 81 108
Circle -10899396 true false 116 41 127
Circle -10899396 true false 60 30 120
Circle -10899396 true false 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.0.3
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@

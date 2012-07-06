LinkedTree-Parser algo design.
renjithforever@gmail.com
20/06/2011

===================================
[i]match: the process of trying to match an input subsequence to a given grammar rule
----
[1]Negetive match_
	happens when an `match` fails, required conditions are given below.
	
	[.1]input pointer reaches end of input AND rule pointer has not reached the end 
		AND `cleen Flag` is not raised(significance of `cleen flag` will be discussed below).
	[.2]rule pointer reaches the end AND no. of `matched terms` is equalt to zero.(not sure when this may happen ..!)

[2]Positive match_
	happens when a `match` is successfull, conditions are given below.

	[.1]rule pointer reaches end AND matched terms > 0.
		** if last rule term is a cleen(*) term then start and continue on a cleen loop untill a non matching input happens.
		** if the last rule term is positive(+) term then start and continue a positive loop untill a non matching term
		   happens AND no of matched terms >0


[3] Search algorith design:_

	^any_number_of_non_matching_terms_(pre-non-match)-FOLLOWED-BY-MATCHING-TERMS-followed_by_any_number_of_non_matching_terms_		(post-non-match)_$

	^[pre-non-match][MATCH][post-non-match]$

	[.1] a `input pointer` shows the current term in the input under study.
	[.2] a `rule pointer` shows the current term in the current garmmar rule.
	[.3] every iteration will check if the term pointed to by `rule pointer` 
		 equals the term pointed by the `input pointer`
	[.4] every iteration may or may not increment the `rule pointer` or `input pointer`

		[.1] if the rule terms donot contain any postive or cleen terms then, 
			 when the rule term matches the input term the `rule pointer` and
			 `input pointer` are incremneted by 1, and the matched term is added 
			 to the `matched temrs` list

		[.2] if rule terms contain one or more cleen  terms and the current 
			 rule term is a cleen term then:

			[.1] if rule term and input term matches.the term is added to `matched terms`,
			     the `input pointer` is incremented,the rule term is not incremnted, 
				 `cleen flag` is raised, and essentially a `cleen loop` is in place.
				 
				 The `cleen loop` allows more input terms of the same rule term to be matched
				 again and again.

				 Every iteration with `cleen flag` ie. in cleen loop incremnts the `input pointer`
				 only.matched input terms are added to `matched terms`

				 In a `cleen loop` the cleenFalg is carried to the next iteration also.

				 
				 When a input term doesnt match the cleen rule term:
				 there are few spl cases, as cleen means 0 or more matches..which is tricky!
					
					[.1]Current cleen term hasnt found a match yet(ie last term in `matched term` list
						is not the current cleen term) and `matched terms` list is empty: 
						here the `input pointer` alone is incremented, the cleenFlag 
						is kept.This leads to basically a search for the cleen term till end of input or till 
						a term matches. That is we need to find the initial hoook, we need re-try the input 
						as there can be false hooks when the first rule term is a cleen term.

						When the end of input reaches, we can clearly say that the cleen term doesnt appear in the input.
						thus we need to search the input again for the next rule term.
						Thus the `input pointer` is reset and the rule pointer is incremented, the cleenFlag is dropped.

					[.2]Current cleen term has 0 matches but `matched` terms list is not empty:
						This shows that the grammar rule has been hooked previously and thus need to be checked for
						completeness only.
						in this case we should not do a complete search for the current cleen term.Look once, if not found
						incremnt `rule pointer`.so that is '0 or more' matches!

					[.3]The cleen term has 1 or more matches (ie. the last term in `matched term` list is the current
						cleen term):This would mean that the cleen loop has terminated. Thus its time to go  
						to the next rule. `rule pointer` is incremented, cleenFlag is dropped.
				 
				 
			
			[.2] if in the current iteartion, the `cleen flag` is down and the current rule term is
				 a cleen term then, we repeat the the iteration with with the cleen flag raised, other 
				 state vars are not changed.

				 This means even if no cleen term macthes , a `cleen loop` is started. This helps to club
				 a zero matched cleen and a `cleen loop` termination.

                 A zero matched cleen is when the rule term is cleen and the input term doesnt match, and
				 `matched terms` for the cleen are zero.

				----------------------zero matched cleen.
				 [cs]:cleenFlag=0
				 [r]: A* B C
					  ^
				 [i]: B C
				      ^
				 [tm]:-ve
				 [ns]:cleenFlag=1

				  Here a `cleen loop` is started, even though there was no match.

				  A `cleen loop` termination is when a cleen term has matched a few inputs
				  previosly(ie `matched terms` >0) but the current itearation the
				  input term doesnt match the cleen term.
				
				-----------------------cleen loop termination.
				  [cs]:cleenflag=1	
				  [r]: A* B C
				       ^
				  [i]: A A A A B C
				               ^
				  [tm]:-ve
				  [ns]:rp,cleenFalg=0

				  With this clubbing when a `zero matched cleen` or a 'cleen loop termination' happens
				  for the next iteration the `rule pointer` is incremented and `cleen flag` is dropped.
				
		
		[.3] if the rule term contains one or more positive term and current rule term is a positive term.

			[.1] with Positive rule term, same flow as a cleen term is taken;as in kleen terms, 
				 multiple input matching runs are called `positive loops`;only exception is that
				 atleast one `input term` should match the rule term(which is basically the definition
				 of a positve closure).

			[.2] To do this, when a rule term(positive) and input term donot match, the last term in the `matched terms`
				 list is checked with rule term(this makes sure atleast one input term was matched previously).
				 If equal the `rule pointer` and `input pointer` are both incremented.
				 Thus breaking the `positive loop`.
				 Else, there can be two possible flows.
					
					[.1] check is `matched terms` list is empty; if empty that means we are not in a 
						possible match sequence and should simply increment the `input pointer`(pre-non-match tersm).

					[.2] if list is not empty, it means this possible match sequence is not good enough
						any more . Thus we need to backtrack on the rule terms. reset the `rule pointer`
						and the `matched terms` list.

				--------------------
				  [cs]:positiveFlag=0,mtl=0	
				  [r]: A+ B C
				       ^
				  [i]: B C
				       ^
				  [tm]:-ve,
				  [ns]:ip+1


				--------------------
				  [cs]:positiveFlag=1,mtl>0,mtl[::-1]==A
				  [r]: A+ B C
				       ^
				  [i]: A A B C
				           ^ 
				  [tm]:-ve,
				  [ns]:rp+1,positiveFlag=0

				--------------------
				  [cs]:mtl>0,mtl[::-1]==S
				  [r]: S A+ B C
				         ^
				  [i]: S B C
				         ^ 
				  [tm]:-ve,
				  [ns]:rp=0(reset),mtl=0

	   [.4]When the rule terms contains 0 or more positive/cleen terms but the current
			rule term is not a cleen/positive term;

			[.1]when `matched tersm` list is 0 and rule term donot match input term, just incremnt
				`input pointer` (pre-non-match).
			[.2] when `matched terms` list>0 then back track on rule terms.reset `rule pointer`
				 and `matched terms` list

			



	[.3] all `pre-non-macth` input terms are skipped by incrementing the `input pointer`
	[.4] all `post-non-match` input terms are skipped automatically by returining TRUE as per `Positive match` conditions.
	[.5]


-------0
[cs]:
[R]:A B C
    ^
[I]:X Y Z A B C
	      ^
[M]:+ve
[ns]:rp+1,ip+1,cleenflag=0

--------1

[4] Search algorithm skeleton:

	if (conditions for no match are true):
		return 0
	elif (conditions for seq-match are true):
		return 1
	elif(kleen loop):
		if (termMatch):
			--do stuff
		else:
			--do stuff

	elif(positive loop):
		if (termMatch):
			--do stuff

	elif(positive/cleen term):
		-do stuff
	elif(Simple term):
		if (termMatch)

	else:
		return -1



"""


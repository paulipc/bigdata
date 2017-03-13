#
# Generate neighbours for a vector.
#

gn <- function(x) {
	neighb2 <- list()
	for(i in 1:length(x)) {
		n <- x
		if (x[i] == 0) {
                n[i] <- 1} 
        else {
                n[i] <- 0
        }
		neighb2[[i]] <- n

	}
	return(neighb2)
	
}

#
# Remove tabulist items from neighbours
#

removetabu <- function(tabu,neighbour) {
  tabuindex <- c()
  if (is.null(tabu)) {
    return(neighbour)
  }
  #cat("tää on returnin jälkeen")
  for (i in 1:length(tabu)) {
    for (y in 1:length(neighbour)) {
      if (all(neighbour[[y]] == tabu[[i]])) {
        tabuindex <- c(tabuindex,y)
      }
    }
    
  }
  
  # remove tabulist items from the result
  neighbour[tabuindex] <- NULL
  return(neighbour)
}

# first initiate values

penalty <- 2
v <- c(135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240)
w <- c(70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120)
tabulist <- NULL
iterations <- 30
x <- c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
memory <- 10
W <- 750
neigh <- NULL
allmaxvalue <- NULL
allmaxweight <- NULL

#
# Main loop:
# Calculate maxvalue and add item to tabulist
#

for(i in 1:iterations) {
    #cat("iteration: ",i,"\n")
    #cat("tabulist: ", tabulist,"\n")
    cat("START##################: ",i,"\n")
    neigh <- gn(x)
    neigh <- removetabu(tabulist, neigh)
    #x <- CountSums(neigh,v,w,penalty,memory,W)
    #########
    # count sums and find index of maxvalue item in neigh
    maxsumv <- 0
    maxsumw <- 0
    lengthneigh <- length(neigh)
    #################
    for(j in 1:lengthneigh) {
        sumv <- sum(neigh[[j]]*v)
        sumw <- sum(neigh[[j]]*w)
        # if total value of this neighbour is biggest
        # then we need to see weight and give penalty when needed.
        if (sumv > maxsumv) {
            # count penalty if weight is over W
            if (sumw > W) {
                sumv <- sumv-penalty*(sumw-W)
            }
        }
        # if value is still bigger than maxvalue then record that values and indexes
        if (sumv > maxsumv) {
            maxsumv <- sumv
            maxsumw <- sumw
            sumindex <- j
        }

    }
    # this is just for testing if we found the right one.
    if (i==24){
        cat(neigh[[sumindex]],"\n")
        cat(neigh[[sumindex]],"\n")
        
    }
    ####################
    cat("sum weight",maxsumw,"\n")
    cat("sum value",maxsumv,"\n")
    allmaxvalue <- c(allmaxvalue,maxsumv)
    allmaxweight <- c(allmaxweight,maxsumw)
    # add result to tabulist
    # cat("neigh[sumindex] ",neigh[sumindex],"\n")
    tabulength<-length(tabulist)+1
    tabulist[tabulength] <- neigh[sumindex]
    #cat("tabulist length",length(tabulist),"\n")

    # drop oldest value from tabulist
    if (length(tabulist) > memory) {
    tabulist[[1]] <- NULL
    }
    # print the result after each iteration
    # cat("sum ",maxsumv,"\n")
    # cat("item", neigh[[sumindex]],"\n")
    # return(neigh[[sumindex]])
    x<-unlist(neigh[sumindex])
    #########
}
cat("Max value  ", max(allmaxvalue),"\n")
cat("Max weight ", max(allmaxweight),"\n")


# RESULT
# iteration:  24 gives us 
# weight 749, which is lower than 750 
# sum value 1458, which is max value when weight is max 750
# 
# just to check in Excel:

1	0	1	0	1	0	1	1	1	0	0	0	0	1	1	item values	
135	139	149	150	156	163	173	184	192	201	210	214	221	229	240	value	
70	73	77	80	82	87	90	94	98	106	110	113	115	118	120	weight	
135		149		156		173	184	192					229	240	1458	sumweight
70		77		82		90	94	98					118	120	749	    sumvalue

# which is correct!

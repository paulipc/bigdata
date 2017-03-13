#
# Excercies 1:
#


#
# Calculates Euclidian distances for all in haberman dataframe to new col
#
EuclDist <- function (haberman, x){
    haberman$dist <- 0 # new col for dist, init to 0
    count <- nrow(haberman)
    for(i in 1:count){
        haberman[i,5] <- sqrt((haberman[i,1] - x[1])^2+(haberman[i,2] - x[2])^2+(haberman[i,3] - x[3] )^2)
    }
    return(haberman)
}

#
# Counts votes for class1 and class2 in ordered dataframe 
#
DoVote <- function(newh,k) {
    CountClass1 <- 0
    CountClass2 <- 0
    for(i in 1:k){
        if (newh[i,4] == 1) {CountClass1 <- CountClass1 + 1}
        if (newh[1,4] == 2) {CountClass2 <- CountClass2 + 1}
    }
    if (CountClass1 > CountClass2) {
        cat("New datapoint belongs to class = 1")
        return(1)
    } else {
        cat("New datapoint belongs to class = 2")
        return(2)
    }
}

#
# Functions are defined and then we just need to call them to get the class for the new datapoint.
#
haberman <- read.csv("haberman.csv")
k <- 8 # this is form assignment
x <- c(63,59,2) # new point from assignment
newh <- EuclDist(haberman, x)
OrderedHaberman <- newh[order(newh$dist),] # order by distance and take 8 first distances for vote
x<-c(x,DoVote(OrderedHaberman,k)) # vote based on 8 first distances in dataframe i.e. 8 closest neighbours
x


#
# Excercies 2:
#


# The network optimization problem
# Excercise 2a

f.obj_transp <- c(3,5,2,9,10,7,5,6,4)

f.con_transp <- matrix (c(1,1,1,0,0,0,0,0,0,
                          0,0,0,1,1,1,0,0,0,
                          0,0,0,0,0,0,1,1,1,
                          1,0,0,1,0,0,1,0,0,
                          0,1,0,0,1,0,0,1,0,
                          0,0,1,0,0,1,0,0,1), nrow=6, byrow=TRUE)
f.dir_transp <- c("<=", "<=","<=", "=", "=", "=")
f.rhs_transp <- c(200,100,150,150,150,150)

solution_transp <- lp ("min", f.obj_transp, f.con_transp, f.dir_transp, f.rhs_transp)

solution_transp$objval

solution_transp$solution

# RESULT for 2a

> solution_transp$objval
[1] 2150
> 
> solution_transp$solution
[1] 150   0  50   0   0 100   0 150   0
>

optimal cost value: 2150
optimal allocation of capacities on the different connections: 150   0  50   0   0 100   0 150   0

# Excercise 2b

# current costs for b are 9,10,7 and 40% decreased values are circa 5,6,4
# new values are updated to code current: f.obj_transp <- c(3,5,2,9,10,7,5,6,4)
# new: f.obj_transp <- c(3,5,2,5,6,4,5,6,4)

f.obj_transp <- c(3,5,2,5,6,4,5,6,4)

f.con_transp <- matrix (c(1,1,1,0,0,0,0,0,0,
                          0,0,0,1,1,1,0,0,0,
                          0,0,0,0,0,0,1,1,1,
                          1,0,0,1,0,0,1,0,0,
                          0,1,0,0,1,0,0,1,0,
                          0,0,1,0,0,1,0,0,1), nrow=6, byrow=TRUE)
f.dir_transp <- c("<=", "<=","<=", "=", "=", "=")
f.rhs_transp <- c(200,100,150,150,150,150)

solution_transp <- lp ("min", f.obj_transp, f.con_transp, f.dir_transp, f.rhs_transp)

solution_transp$objval

solution_transp$solution


# RESULT for 2b

> solution_transp$objval
[1] 1850
> 
> solution_transp$solution
[1] 150   0  50   0 100   0   0  50 100

# Decrasing 40% of source B shipping cost will decrease total cost from 2150 to 1850.

# solution a)
> solution_transp$solution
[1] 150   0  50   0   0 100   0 150   0

# solution b)
> solution_transp$solution
[1] 150   0  50   0 100   0   0  50 100

supply from B->Y increases 0->100 (shipping cost was 10 and now is only 6)
supply from B->Z decreases 100->0 (shipping cost was 7 and now is only 4, total shipping is now cheaper from B)
supply from C->Y decreases 150->50
supply from C->Z increases 0->100

# Excercise: separate paper with transshipment problem

f.obj_transs <- c(3,2,3,5,6,2,8,10,5,9,12,15)
f.con_transs <- matrix(c(1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,
                         0,	0,	0,	1,	1,	-1,	0,	0,	0,	0,	0,	0,
                         0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,
                         0,	-1,	0,	-1,	0,	0,	-1,	0,	1,	1,	0,	0,
                         0,	0,	-1,	0,	-1,	0,	0,	-1,	0,	0,	1,	1,
                         1,	0,	0,	0,	0,	0,	0,	0,	1,	0,	1,	0,
                         0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	1), nrow=7, byrow=TRUE)
f.dir_transs <- c("<=", "<=", "<=", "=", "=", "=", "=")
f.rhs_transs <- c(500,400,300,0,0,600,600)

solution_transs <- lp ("min", f.obj_transs, f.con_transs, f.dir_transs, f.rhs_transs)

solution_transs$objval

solution_transs$solution

# result for separate page transshipment problem
> solution_transs$objval
[1] 11500
> 
> solution_transs$solution
 [1] 500   0   0 700   0 300   0   0 100 600   0   0

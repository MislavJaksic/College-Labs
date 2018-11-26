## Lab Two

Implemented all five algorithms:  

Unimodal interval search:  
*  find the direction in which the valley is located.
*  descent down to the valley.
*  return the interval within which the valley is located.

Golden section search:  
*  create four points, ABCD.
*  eliminate the highest point.
*  repeat until you reach the valley floor.
*  return the lowest point of the valley.

Coordinate descent:  
*  construct a one dimensional function.
*  find the valley of the function.
*  repeat until you have reached a valley in all dimensions.
*  return the lowest point of the valley.
  
Nelder Mead method:  
*  create a simplex.
*  move the simplex points using reflection, expansion and contraction.
*  repeat until all the simplex points bunch up.
*  return the lowest point of the valley.

Hooke Jeeves method:  
*  move a point in all directions.
*  reflect a point across the moved point.
*  move and reflect until they can no longer move the point towards the valley floor.
*  return the lowest point of the valley.

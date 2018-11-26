## Lab Three

Implemented all four algorithms.  

Gradient descent:  
*  calculate the gradient.
*  calculate where to move along the gradient.
*  move the point along the gradient.
*  repeat until divergence or the gradient becomes small.
*  return the final coordinate.

Newton-Raphson method:  
*  calculate the gradient.
*  calculate the Hessian matrix.
*  calculate where to move along the gradient using the Hessian matrix.
*  move the point along the gradient.
*  repeat until divergence or the gradient becomes small.
*  return the final coordinate.
  
Box method:  
*  put the point within constraints.
*  create a polygon.
*  move a polygon point making sure it never breaks a constraint.
*  repeat until moving can no longer move the point towards the valley floor.
*  return the final coordinate.
  
Constrained problem transformation:  
*  create a replacement function.
*  optimize the replacement function.
*  return the final coordinate.
  

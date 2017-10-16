# https://github.com/joowani/binarytree/blob/master/binarytree/__init__.py
# shows the binary tree with ASCII characters routine

class ALV(object):
  
  def __init__(self):
    self.root = False
  
  def search(self, value):
    """Same as in ordinary binary tree"""
    pass
    
  def add(self, value):
    if self.root:
      pass
      self._Balance()
    else:
      self.root = AVLNode(value)
  
  def delete(self, value):
    """"""
    pass
    self._Balance()
    
  def _Balance(self):
    """"""
    pass
    
  def __str__(self):
    """str(tree) and print tree"""
    
    
class AVLNode(object):
  def __init___(self, value):
    self.value = value
    self.balanceFactor = 0
    self.leftChild = False
    self.rightChild = False

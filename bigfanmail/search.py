class EAddress:

   def __init__(self, eaddress):
      self.isregistered = 1 
      self.try_eaddress = [] 
      self.plan = ' '
      self.eaddress = eaddress

   def is_registered(self):
      return self.isregistered

   def set_is_registered(self, isreg):
      self.isregistered = isreg

   def set_try_eaddress(self, domain):
      self.try_eaddress.append(self.eaddress + '@' + domain)

   def set_plan(self, plan):
      self.plan = plan

   def get_try_eaddress(self):
      return self.try_eaddress

   def get_eaddress(self):
      return self.eaddress

   def get_plan(self):
      return self.plan



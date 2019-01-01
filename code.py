import gi
gi.require_version('Gtk', '3.0')
import matplotlib.pyplot as plt
from gi.repository import Gtk
from threading import Thread
from random import randint

"""
This code was written by Bensaada Abdel Kamal
If you have any suggestion to improve the code i'd be happy
email: abdelkamalbensaada@gmail.com

The code basically runs battles between your Hero and a Monster and plots the winrate using matplotlib
each one has 4 attributes (Atk, critacal chance, critical damage, health)
the 1st set of 4 text boxes define: Atk, CritC, CritDmg, Health for the Hero
the 2nd set of 4 text boxes define: Atk, CritC, CritDmg, Health for the Monster
the last set of boxes sets the simualtion arguments
click on the start simualtion button start the calculations

The project depends on:
PyGobject
matplotlib
"""

class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Fight Winrate Plotter')
		self.set_border_width(10)
		self.set_size_request(200, 100)
	
		#box
		self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		self.add(self.box)

		#button
		self.button=Gtk.Button(label="--Start Simualtion--")
		self.button.connect("clicked",self.button_clicked)
		self.box.pack_start(self.button, True, True, 0)
		
		self.label = Gtk.Label("Change The values to suite your simualtion")
		self.box.pack_start(self.label, True,True,0)

		self.HeroAtk = self.create_text_and_label("Hero's Attack Power:","20")[0]
		self.HeroCritC = self.create_text_and_label("Hero's Critical Chance:","50")[0]
		self.HeroCritDmg = self.create_text_and_label("Hero's Critical Damage:","200")[0]
		self.HeroHealth = self.create_text_and_label("Hero's Health:","10000")[0]

		self.EnemyAtk = self.create_text_and_label("Monster's Attack Power:","20")[0]
		self.EnemyCritC = self.create_text_and_label("Monster's Critical Chance:","50")[0]
		self.EnemyCritDmg = self.create_text_and_label("Monster's Critical Damage:","200")[0]
		self.EnemyHealth = self.create_text_and_label("Monster's Health:","10000")[0]
		
		self.Attribute=self.create_text_and_label("Select an attribute: (Atk , CritC, CritDmg)","Atk")[0]
		self.NumberOfIterations=self.create_text_and_label("Number Of iterations (Number of steps):","40")[0]
		self.NumberOfBattels=self.create_text_and_label("Number of battles per iteration:","500")[0]
		self.Step=self.create_text_and_label("The step between each iteration:","5")[0]


	def create_text_and_label(self,labeltext,text):
		self.label =Gtk.Label(labeltext)
		self.box.pack_start(self.label, True,True,0)
		self.entry=Gtk.Entry()
		self.entry.set_text(text)
		self.box.pack_start(self.entry, True, True, 0)
		return self.entry, self.label



	def button_clicked(self,widget):
		HA=int(self.HeroAtk.get_text())
		HCC=int(self.HeroCritC.get_text())
		HCD=int(self.HeroCritDmg.get_text())
		HH=int(self.HeroHealth.get_text())
		EA=int(self.EnemyAtk.get_text())
		ECC=int(self.EnemyCritC.get_text())
		ECD=int(self.EnemyCritDmg.get_text())
		EH=int(self.EnemyHealth.get_text())
		NOB=int(self.NumberOfBattels.get_text())
		NOI=int(self.NumberOfIterations.get_text())
		S=float(self.Step.get_text())
		ATT=str(self.Attribute.get_text())
		Hero = chara(HA,HCC,HCD,HH)
		Monster= chara(EA,ECC,ECD,EH)
		try:
			t1 = Thread(target=Hero.Plot2DBattels , args=(Monster, NOB,NOI,S,ATT))
			t1.start()
		except Exception as e:
			print(e)

class chara():
	def __init__(self, Atk,CritC, CritDmg ,Health):
		self.Atk=Atk
		self.CritC=CritC
		self.Health=Health
		self.CritDmg= CritDmg

	def iscrit(self):
		if randint(0,100)<=self.CritC:
			return True
		else:
			return False

	def whostarts(self, enemy):
		if randint(0,1):
			return sellf
		else:
			return enemy

	def fight(self, enemy):
		if self.Health>0:
			self.attack(enemy)
			enemy.fight(self)
	
	def whowon(self, enemy):
		if self.Health>0 and enemy.Health<=0:
			return 1
		elif enemy.Health>0 and self.Health<=0:
			return -1
	
	def Battle(self,enemy):	
		if self.whostarts is self:
			self.fight(enemy)
		else:
			enemy.fight(self)
		return self.whowon(enemy)
	
	def attack(self, enemy):
		if self.iscrit():
			enemy.Health -= self.Atk*(self.CritDmg/100)
		else:
			enemy.Health-=self.Atk

	def nBattles(self, enemy, NumberOfBat):
		InAHealth =self.Health
		InBHealth =enemy.Health
		Awins=0
		for i in range(NumberOfBat):
			self.Health=InAHealth
			enemy.Health= InBHealth
			if self.Battle(enemy) == 1:
				Awins+=1
			else:
				Awins+=0
		winrate = Awins/NumberOfBat
		return winrate

	def nBattlesWithSteps(self,enemy,NumberOfBat, NumberOfIt , step, Attribute):
		Attribute_type=['Atk', 'CritC', 'CritDmg']
		if Attribute not in Attribute_type:
			raise ValueError("Invalid attribute type. Expected one of: %s" % Attribute_type)
		result=[]
		Ainput=[]
		InAHealth =self.Health
		InBHealth =enemy.Health
		if Attribute == 'Atk':
			for index in range(NumberOfIt):
				self.Health=InAHealth
				enemy.Health=InBHealth
				result.append(self.nBattles(enemy,NumberOfBat)) 
				Ainput.append(self.Atk)
				self.Atk+=step
			return Ainput, result
		elif Attribute == 'CritC':
			for index in range(NumberOfIt):
				self.Health=InAHealth
				enemy.Health=InBHealth
				result.append(self.nBattles(enemy,NumberOfBat)) 
				Ainput.append(self.CritC)
				self.CritC+=step
			return Ainput, result
		elif Attribute == 'CritDmg':
			for index in range(NumberOfIt):
				self.Health=InAHealth
				enemy.Health=InBHealth
				result.append(self.nBattles(enemy,NumberOfBat)) 
				Ainput.append(self.CritDmg)
				self.CritDmg+=step
			return Ainput, result

	def Plot2DBattels(self,enemy,NumberOfBat, NumberOfIt , step, Attribute):
		inp, res = self.nBattlesWithSteps(enemy,NumberOfBat,NumberOfIt,step,Attribute)
		plt.plot(inp,res)
		plt.show()
 
def main():
	window = MainWindow()
	window.show_all()
	window.connect("destroy", Gtk.main_quit)
	Gtk.main()

if __name__ == '__main__':
	main()
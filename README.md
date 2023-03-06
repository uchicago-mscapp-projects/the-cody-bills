# The Cody Bills: 
## Analyzing The Energy Policy of US's 

Is the legislation of a state highly related to the main economic activities of that state? We do not intend to answer this question entirely but in this project, we explore a framework to analyze how frequent a specific topic was discussed in the bills proposed in two states: Texas, and Pennsylvania. For these states, we know that they are the two big energy producers in the United States, in fact, they are the two main producer states for 2020 with 23,329 trillion btu and 9,492 trillion btu per the U.S. Energy Information Administration. Consequently, we use our algorithms to explore the presence of energy related bills proposed by Texas’ and Pennsylvania’s congressional representatives.

## Insturctions to execute project codes 

**NOTE**: All codes to be run from within the project root directory

1) Clone the repository into your server 

``git clone https://github.com/uchicago-capp122-spring23/30122-project-the-cody-bills.git``

2)	Set up the virtual environment to install all the packages or dependencies used in the project by running command ``poetry install``, and activate the virtual environment running ``poetry shell``

3)	 To run the main dashboard of the project run 

``python -m cody_bills``

4)	If you want to recreate the intermediate steps

    a) To collect the Bills we used for Pennsylvania and Texas, run:

``line of code``

    b) To clean the bills and conduct the text analysis (word-clouds and Energy Policy index calculation), run:

``python -m cody_bills.Text_Preprocessing.text_analysis``

    c) To generate the graphs comparing the states across several Energy policy indicators, run:

``line of code``

## Interacting with the Dashboard
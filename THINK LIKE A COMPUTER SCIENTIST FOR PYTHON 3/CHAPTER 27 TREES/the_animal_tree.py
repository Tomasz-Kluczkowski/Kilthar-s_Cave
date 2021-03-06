import record_tree_to_file_animal
from record_tree_to_file_animal import Tree


def yes(ques):
    ans = input(ques).lower()
    try:
        return ans[0] == "y"
    except IndexError:
        yes(ques)


def animal():
    # start with already gained knowledge from previous questions
    try:
        root = record_tree_to_file_animal.file_to_tree("animal_data.txt")
        record_tree_to_file_animal.print_tree_indented(root)
    except FileNotFoundError:
        root = Tree("bird")
    # loop until user quits
    while True:
        print()
        if not yes("Are you thinking of an animal? "): break

        # walk the tree
        tree = root
        while tree.left is not None:
            prompt = tree.cargo + "? "
            if yes(prompt):
                tree = tree.right
            else:
                tree = tree.left

        # make a guess
        guess = tree.cargo
        prompt = "Is it a " + guess + "? "
        if yes(prompt):
            print("I rule!")
            continue

        # get new information
        prompt = "What is the animal's name? "
        animal = input(prompt)
        prompt = "What question would distinguish a {0} from a {1} ? "
        question = input(prompt.format(animal, guess))

        # add new information to the tree
        tree.cargo = question
        prompt = "If the animal were {0} the answer would be? "
        if yes(prompt.format(animal)):
            tree.left = Tree(guess)
            tree.right = Tree(animal)
        else:
            tree.left = Tree(animal)
            tree.right = Tree(guess)
    # store gained knowledge for future use
    # if at least initial branches of the root are filled with data
    if root.left is not None and root.right is not None:
        record_tree_to_file_animal.tree_to_file(root, "animal_data.txt")


animal()

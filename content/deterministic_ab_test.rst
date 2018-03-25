Deterministic A/B tests via the hashing trick
#############################################
:date: 2018-03-20 08:30
:author: Chris Stucchio
:tags: ab testing, computer science
:canonical: https://medium.com/simpl-under-the-hood/deterministic-a-b-tests-via-the-hashing-trick-d1ea49483202

In principle A/B testing is really simple. To do it you need to define two separate user experiences, and then randomly allocate users between them::

    def final_experience(user):
        if random.choice([0,1]) == 0:
            return user_experience_A(user)
        else:
            return user_experience_B(user)

So far this seems pretty simple. But then you think about edge cases:

- Shouldn't the same user get the same experience if they do this twice?
- After the test is complete, how can I compare group A and b?

It's not hard to track this data, but it certainly makes your code a bit uglier::

    def final_experience(user):
        user_variation = db.run_query("SELECT user_variation FROM users WHERE user_id = ?", user.id)
        if user_variation == 0: # If the user already saw a variation, show them the same one
            return user_experience_A(user)
        elif user_variation == 1:
            return user_experience_B(user)
        else: #No record in the DB
            user_variation = random.choice([0,1])
            db.run_query("INSERT INTO user_variation (user_id, variation) VALUES (?, ?)", user.id, user_variation)
            if user_variation == 0:
                return user_experience_A(user)
            else:
                return user_experience_B(user)

This is doable, but the code is a lot longer and more annoying. Are there race conditions? Should everything live in a single transaction, potentially skewing things?

Fortunately there's a better way: the hashing trick.::

    def deterministic_random_choice(user_id, test_name, num_variations):
        """Returns a 'random'-ish number, between 0 and num_variations,
           based on the user_id and the test name.

           The number will not change if the user_id and test name
           remain the same.
           """
       return (hash(user_id + test_name) % num_variations)

    def final_experience(user):
        if deterministic_random_choice(user.id, "experience_test", 2) == 0:
            return user_experience_A(user)
        else:
            return user_experience_B(user)

Usingdeterministic_random_choice instead of random.choice will ensure that the same user is always assigned to the same variation. This is done without any database access.

It also makes it very easy to run analytics and compare the two groups, even though we never stored group membership in any database table::

    SELECT SUM(user.revenue), COUNT(user.id), deterministic_random_choice(user.id, "experience_test", 2)
            FROM users
            WHERE user.signup_date > test_start_date
          GROUP BY deterministic_random_choice(user.id, "experience_test", 2)

(This is not SQL that any real DB will actually run, but it's illustrative.)

Whatever you currently do for analytics, you can take the exact same queries and either GROUP BY the deterministic_random_choice or else run the query once for each variation and put deterministic_random_choice(user.id, "experience_test", 2) = 0,1 into the WHERE clause.

It's just a nice simple trick that makes it easy to start A/B testing today. No database migration in sight!

This post was first published on the `Simpl company blog <https://medium.com/simpl-under-the-hood/deterministic-a-b-tests-via-the-hashing-trick-d1ea49483202>`_.

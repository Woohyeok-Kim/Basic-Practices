from manim import *
import numpy as np

config.pixel_height = 1080  # Set height for 1080p
config.pixel_width = 1920   # Set width for 1080p
config.frame_rate = 60      # Optionally, you can also increase the frame rate for smoother animations


class TalentProjection(ThreeDScene):  # Change Scene to ThreeDScene for 3D support
    def construct(self):
        # Set up the 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Create and display the 3D axes
        axes = ThreeDAxes()
        self.play(Create(axes))

        # Create 3 social norm vectors with a random z component
        social_norms = [
            np.array([3, 1, np.random.uniform(-3, 3)]),  # Social Norm 1
            np.array([1, 3, np.random.uniform(-3, 3)]),  # Social Norm 2
            np.array([2, 2, np.random.uniform(-3, 3)])   # Social Norm 3
        ]
        
        social_vectors = VGroup()
        colors = [BLUE, GREEN, RED]
        labels = ['Norm 1', 'Norm 2', 'Norm 3']

        # Add the social norm vectors to the scene
        for i, norm_vector in enumerate(social_norms):
            vec = Arrow(ORIGIN, norm_vector, color=colors[i], buff=0)
            social_vectors.add(vec)
            self.play(Create(vec), run_time=1)
            # Label each norm
            norm_label = MathTex(labels[i]).next_to(vec.get_end(), RIGHT)
            self.play(Write(norm_label))

        self.wait(1)

        # Generate random individual vectors (talent vectors) with random z component
        individuals = VGroup()
        np.random.seed(42)
        for _ in range(30):
            random_direction = np.random.uniform(-3, 3, size=2)
            z_component = np.random.uniform(-5, 5)  # Add a random z component
            vector = Arrow(ORIGIN, np.append(random_direction, z_component), buff=0)
            individuals.add(vector)

        # Add individual talent vectors to the scene
        self.play(AnimationGroup(*[Create(vec) for vec in individuals], lag_ratio=0.1))

        self.wait(2)

        # Prepare projections in parallel
        transformations = []
        for ind_vector in individuals:
            # Choose a random social norm to project onto
            chosen_norm = social_norms[np.random.randint(0, 3)]
            
            # Perform projection in 3D
            projection = np.dot(ind_vector.get_end(), chosen_norm) / np.linalg.norm(chosen_norm) ** 2 * chosen_norm
            
            # Shrink the vector and align with the norm
            new_vector = Arrow(ORIGIN, projection, buff=0, color=ind_vector.get_color()).scale(0.5)
            
            # Store the transformation for simultaneous animation
            transformations.append(Transform(ind_vector, new_vector))

        # Apply all transformations at the same time
        self.play(AnimationGroup(*transformations, lag_ratio=0))

        self.wait(2)

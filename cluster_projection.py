from manim import *
import numpy as np
from sklearn.cluster import KMeans

config.pixel_height = 1080  # Set height for 1080p
config.pixel_width = 1920   # Set width for 1080p
config.frame_rate = 60      # Optionally, you can also increase the frame rate for smoother animations

class ClusterProjection(ThreeDScene):
    def construct(self):
        # Set up the 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Step 1: Create and display the 3D axes
        axes = ThreeDAxes()
        self.play(Create(axes))

        # Step 2: Generate random individual vectors (talent vectors) with random z component
        individuals = VGroup()
        np.random.seed(42)
        individual_vectors = []
        for _ in range(30):
            random_direction = np.random.uniform(-3, 3, size=2)
            z_component = np.random.uniform(-1, 1)  # Add a random z component
            vector = np.append(random_direction, z_component)
            individual_vectors.append(vector)
            individuals.add(Arrow(ORIGIN, vector, buff=0))

        # Add individual talent vectors to the scene
        self.play(AnimationGroup(*[Create(vec) for vec in individuals], lag_ratio=0.1))

        self.wait(2)

        # Step 3: Cluster the individual vectors (use KMeans for clustering)
        kmeans = KMeans(n_clusters=6, random_state=42).fit(individual_vectors)  # Use 6 clusters for diversity
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_

        # Create representative vectors for each cluster (centroid vectors) with distinction
        representative_vectors = VGroup()
        cluster_colors = [BLUE, GREEN, RED, ORANGE, PURPLE, YELLOW]  # More colors for more clusters

        # Step 4: Add some effects to emphasize the formation of clusters
        for i, centroid in enumerate(centroids):
            cluster_vectors = VGroup(
                *[individuals[j] for j in range(len(individuals)) if labels[j] == i]
            )
            self.play(cluster_vectors.animate.set_color(cluster_colors[i]))  # Color the vectors in the cluster
            
            # Create cluster representative (centroid)
            centroid_vector = Arrow(ORIGIN, centroid, color=cluster_colors[i], buff=0, stroke_width=8, tip_length=0.35)
            centroid_vector.set_opacity(0.5)  # Distinguish by making it semi-transparent
            representative_vectors.add(centroid_vector)
            self.play(Create(centroid_vector), run_time=1)

        self.wait(1)

        # Step 5: Project individual vectors to the representative vector of their cluster
        cluster_transformations = []
        for i, ind_vector in enumerate(individuals):
            # Get the corresponding centroid for the cluster
            cluster_centroid = centroids[labels[i]]
            
            # Perform projection in 3D
            projection = np.dot(ind_vector.get_end(), cluster_centroid) / np.linalg.norm(cluster_centroid) ** 2 * cluster_centroid
            
            # Shrink the vector and align with the cluster representative
            new_vector = Arrow(ORIGIN, projection, buff=0, color=ind_vector.get_color()).scale(0.5)
            
            # Store the transformation for simultaneous animation
            cluster_transformations.append(Transform(ind_vector, new_vector))

        # Apply all transformations at the same time
        self.play(AnimationGroup(*cluster_transformations, lag_ratio=0))

        self.wait(2)
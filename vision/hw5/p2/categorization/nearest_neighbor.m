function index = nearest_neighbor(neighbors, current)
% returns the index in neighbors that has the smallest distance to current
distances = inf(size(neighbors, 2), 1);

for i = 1:size(neighbors, 2)
    distances(i) = norm(neighbors{i} - current);
end

[~, index] = min(distances);

end
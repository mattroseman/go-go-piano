%% Find keys

% Black Keys

[blackKeys,numBlackKeys] = findBlackKeys(keyboard.Bin,...
    cuttingLinesSorted(2)-cuttingLinesSorted(1));

% Plot
figure; imshow(keyboard.RGB,'Border','tight'); hold on;
for i = 1:numBlackKeys
    [r,c] = find(blackKeys == i);
    k = convhull(c,r);
    h = plot(c(k),r(k),'y-');
    set(h,'LineWidth',2);
end

% White keys

[whiteKeys,numWhiteKeys,middle_csharp, middle_c] = ...
    findWhiteKeys(blackKeys,numBlackKeys,size(blackKeys,1));

% Erode black keys to create buffer between white and black
SE = ones(7);
blackKeys = imerode(blackKeys,SE);

original_blackValues = zeros(1,numBlackKeys);
for i = 1:numBlackKeys
    keys = blackKeys == i;
    key_intensity = sum(sum(keys .* keyboard.Gray));
    area = sum(sum(keys));
    original_blackValues(i) = key_intensity / area;
end

original_whiteValues = zeros(1,numWhiteKeys);
for i = 1:numWhiteKeys
    keys = whiteKeys == i;
    %change = sum(sum(keys .* bgDiff));
    key_intensity = sum(sum(keys .* keyboard.Gray));
    area = sum(sum(keys));
    %scoresWhite(i) = change / area;
    original_whiteValues(i) = key_intensity / area;
end

% Plot
figure; imshow(keyboard.RGB,'Border','tight'); hold on;
for i = 1:numWhiteKeys
    [r,c] = find(whiteKeys == i);
    k = convhull(c,r);
    h = plot(c(k),r(k),'y-');
    set(h,'LineWidth',2);
end

% Plot
figure; imshow(keyboard.RGB,'Border','tight'); hold on;
for i = 1:numBlackKeys
    [r,c] = find(blackKeys == i);
    k = convhull(c,r);
    h = plot(c(k),r(k),'y-');
    set(h,'LineWidth',1);
end
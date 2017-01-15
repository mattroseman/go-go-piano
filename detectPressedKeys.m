%% Find keys being pressed

pressedWhite = zeros(numFrames,numWhiteKeys);
pressedBlack = zeros(numFrames,numBlackKeys);

for i = 60:numFrames
    curFrame = framesGray{i};
    curMask = ~framesMask{i};
    if i == 1
        prevFrame = keyboard.Gray;
        prevMask = ~keyboard.Mask;
        prevPressedWhite = pressedWhite(1,:);
        prevPressedBlack = pressedBlack(1,:);
    else
        prevFrame = framesGray{i-1};
        prevMask = ~framesMask{i-1};
        prevPressedWhite = pressedWhite(i-1,:);
        prevPressedBlack = pressedBlack(i-1,:);
    end
    
    [pressedW,pressedB] = pressKeys(curFrame,curMask,prevFrame,prevMask,whiteKeys,numWhiteKeys,original_whiteValues,blackKeys,numBlackKeys,original_blackValues);
    pressedWhite(i,:) = pressedW;
    pressedBlack(i,:) = pressedB;
    %pressedWhite(i,:) = xor(prevPressedWhite,pressedW);
    %pressedBlack(i,:) = xor(prevPressedBlack,pressedB);
end

% Clean up
for i = 60:numFrames
    for j = 1:numWhiteKeys
        if pressedWhite(i,j)
            keys = whiteKeys == j;
            if sum(sum(keys .* framesMask{i})) < 50
                pressedWhite(i,j) = 0;
            end
        end
    end
    
    for j = 1:numBlackKeys
        if pressedBlack(i,j)
            keys = blackKeys == j;
            if sum(sum(keys .* framesMask{i})) < 30
                pressedBlack(i,j) = 0;
            end
        end
    end
end

% Plot
for i = 60:numFrames
    figure(1); imshow(framesRGB{i},'Border','tight'); hold on;
    for j = 1:numWhiteKeys
        if pressedWhite(i,j)
            keys = whiteKeys == j;
            [r,c] = find(whiteKeys == j);
            k = convhull(c,r);
           h = plot(c(k),r(k),'y-');
           set(h,'LineWidth',2);
       end
    end
    for j = 1:numBlackKeys
        if pressedBlack(i,j)
            keys = blackKeys == j;
            [r,c] = find(whiteKeys == j);
            k = convhull(c,r);
            h = plot(c(k),r(k),'y-');
            set(h,'LineWidth',2);
        end
    end
    filename = sprintf('annotated_%03d',i);
    screen2png(filename);
   %pause(0.5);
end

%allPresses = reshape([pressedWhite(:), pressedBlack(:)]', 2*size(pressedWhite, 1), []);
maxLength = max(length(pressedWhite(1,:)),length(pressedBlack(1,:)));
csvOutput = [middle_c zeros([1,maxLength-1]);
             middle_csharp zeros([1,maxLength-1])];
for i = 60:numFrames
    csvOutput = [csvOutput; padarray(pressedWhite(i,:), [0,maxLength-length(pressedWhite(1,:))], 'post'); padarray(pressedBlack(i,:), [0,maxLength-length(pressedBlack(1,:))], 'post')];
    csvOutput = [csvOutput;
                 [pressedWhite(i,:) zeros([1,maxLength-length(pressedWhite(1,:))])];
                 [pressedBlack(i,:) zeros([1,maxLength-length(pressedBlack(1,:))])];
                ];
end

csvwrite('file.file', csvOutput);

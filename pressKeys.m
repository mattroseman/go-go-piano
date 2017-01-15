function [ pressedWhite,pressedBlack ] = pressKeys(frame1,mask1,frame2,mask2,whiteKeys,numWhiteKeys,original_whiteValues,blackKeys,numBlackKeys,original_blackValues)

dxRange = -3:3;
dyRange = -3:3;
[frameAligned,maskAligned,dxOpt,dyOpt] = alignFrame(frame1,mask1,frame2,mask2,dxRange,dyRange);
imgDiff = abs(frame2 - frameAligned);
bgDiff = imgDiff .* min(maskAligned,mask2);
kernel = fspecial('average',3);
bgDiff = imfilter(bgDiff,kernel);
% figure; imshow(bgDiff,'Border','tight'); hold on;

new_frame = frame1 .* min(maskAligned,mask1);

scoresWhite = zeros(1,numWhiteKeys);
intensitiesWhite = zeros(1,numWhiteKeys);
areaWhite = zeros(1,numWhiteKeys);
pressedWhite = zeros(1,numWhiteKeys);
for i = 1:numWhiteKeys
    if i < 4 | i > 6
        continue
    end
    keys = whiteKeys == i;
    %change = sum(sum(keys .* bgDiff));
    key_intensity = sum(sum(keys .* new_frame));
    intensitiesWhite(i) = key_intensity;
    area = sum(sum(keys .* min(maskAligned,mask1)));
    areaWhite(i) = area;
    scoresWhite(i) = key_intensity / area;
    %scoresWhite(i) = key_intensity / area;
    middle = numWhiteKeys / 2;
    value = (original_whiteValues(i) - scoresWhite(i));%*min(i,numWhiteKeys-i);
    %value = scoresWhite(i); 
    if value >= 0.01
%         [r,c] = find(whiteKeys == i);
%         k = convhull(c,r);
%         plot(c(k),r(k),'y-');
        pressedWhite(i) = 1;
    end
end

 %[scoresWhiteSorted,ind] = sort(scoresWhite);
 %figure; plot(1:numWhiteKeys,scoresWhite);
 %disp(scoresWhite);
 %figure; plot(1:numWhiteKeys,intensitiesWhite);
 %disp(intensitiesWhite);
 %figure; plot(1:numWhiteKeys,areaWhite);
 %disp(areaWhite);
 %figure; plot(1:numWhiteKeys,original_whiteValues - scoresWhite);
 %disp(original_whiteValues - scoresWhite);
 
% figure; imshow(bgDiff,'Border','tight'); hold on;

scoresBlack = zeros(1,numBlackKeys);
pressedBlack = zeros(1,numBlackKeys);
for i = 1:numBlackKeys
    keys = blackKeys == i;
    change = sum(sum(keys .* bgDiff));
    %key_intensity = sum(sum(keys .* new_frame));
    %intensitiesBlack(i) = key_intensity;
    area = sum(sum(keys .* min(maskAligned,mask2)));
    areaBlack(i) = area;
    scoresBlack(i) = change / area;
    %scoresBlack(i) = key_intensity / area;
    if scoresBlack(i) >= 0.03
%         [r,c] = find(blackKeys == i);
%         k = convhull(c,r);
%         plot(c(k),r(k),'y-');
        pressedBlack(i) = 1;
    end
end

% [scoresBlackSorted,ind] = sort(scoresBlack);
% figure; plot(1:numBlackKeys,scoresBlackSorted);
% disp(scoresBlackSorted);
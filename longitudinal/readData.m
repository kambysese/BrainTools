%function [sid, long_var, score, score2, predictor, predictor_name, test_name, test_2_name] = readData(data, subs, test_name, test_2_name, time_course, usesessions)
% Function: Prepares data for lmeLongitudinaldata and plotLongitudinaldata
%% Data set
%     If using a Mac/Linux
%       [~, ~, data] = xlsread('~/Desktop/NLR_Scores.xlsx');
%     If using a PC
    [~, ~, data] = xlsread('C:\Users\Patrick\Desktop/NLR_Scores.xlsx');

% gather column headings
data_ref = data(1,:);
% add '\' preceding each "_" for nicer looking titles/formatting
data_ref = strrep(data_ref, '_', '\_');
% remove data headers from data
data = data(2:end,:);
% find all rows for subjects of interest
data_indx_tmp = [];
data_indx     = [];
for subj = 1:numel(subs)
    data_indx_tmp = find(strcmp(data(:, strcmp(data_ref, 'Subject')), subs(subj)));
    data_indx = vertcat(data_indx, data_indx_tmp);
end
% create refined data array for data of interest
% initialize empty arrays
sid = []; sessions = []; days = []; hours = []; predictor = [];

% vertcat each reading test variable
for subj = 1:numel(data_indx)
    sid        = vertcat(sid, data(data_indx(subj), strcmp(data_ref, 'Subject')));
    sessions    = vertcat(sessions, data(data_indx(subj), strcmp(data_ref, 'LMB\_session')));
    days       = vertcat(days, data(data_indx(subj), strcmp(data_ref, 'Time')));
    hours      = vertcat(hours, data(data_indx(subj), strcmp(data_ref, 'Hours')));
    predictor  = vertcat(predictor, data(data_indx(subj), strcmp(data_ref, strrep(predictor_name, '_', '\_'))));
end
predictor = cell2mat(predictor);
% Gather predictor variable
pred_index = []; 
predictor_influx = [];
for subj = 1:numel(subs)
    pred_index = find(strcmp(sid, subs(subj)));
    p_score = NaN;
    for kk = 1:numel(pred_index)
        if predictor(pred_index(kk)) > 0
            p_score = predictor(pred_index(kk));
            
            for jj = 1:numel(pred_index)
                predictor(pred_index(jj)) = p_score;
            end
        end
        
    end
    predictor_influx = vertcat(predictor_influx, predictor(pred_index(1)));
end

predictor = predictor_influx;

% Convert cell arrays to variables suitable for use with dataset()
hours       = cell2mat(hours);
%% Time Course
% Variable Selection
if time_course == 1
    long_var = hours;
elseif time_course == 2
    long_var = days;
    long_var = cell2mat(long_var);
elseif time_course == 3
    long_var = sessions;
    long_var = cell2mat(long_var);
end



%% Gather Reading Score of Interest
% intialize variable
score = []; score2 = [];

% vertcat the data into a cell matrix
for subj = 1:numel(data_indx)
score = vertcat(score, data(data_indx(subj), strcmp(data_ref, strrep(test_names(test), '_', '\_'))));
score2 = vertcat(score2, data(data_indx(subj), strcmp(data_ref, strrep(test_names(test), '_', '\_'))));
end
% Convert reading score to matlab variable
score = cell2mat(score);
score2 = cell2mat(score2);


%% Concentrate on sessions of interest, if applicable
if time_course == 3
    indx = ismember(long_var, usesessions);
    % remove rows that correspond to the ones we don't want to analyze
    sid = sid(indx); long_var = long_var(indx); score = score(indx); 
     score2 = score2(indx); 
end



%return



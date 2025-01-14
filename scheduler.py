from tensorflow import keras


class MomentumScheduler(keras.callbacks.Callback):
    """Momentum rate scheduler.
    # Arguments
    schedule: a function that takes an epoch index as input
    (integer, indexed from 0) and current momentum rate
    and returns a new momentum rate as output (float).
    verbose: int. 0: quiet, 1: update messages.
    """

    def __init__(self, schedule, verbose=0):
        super(MomentumScheduler, self).__init__()
        self.schedule = schedule
        self.verbose = verbose

    def on_epoch_begin(self, epoch, logs=None):
        # if not hasattr(self.model.optimizer, 'lr'):   <=== Original  self.model.optimizer.optimizer._learning_rate
        if not hasattr(self.model.optimizer.optimizer, '_momentum'):
            raise ValueError('Optimizer must have a "_momentum" attribute.')
        try:  # new API
            # lr = float(K.get_value(self.model.optimizer.lr))
            momentum = float(self.model.optimizer.optimizer._momentum)
            momentum = self.schedule(epoch, momentum)
        except TypeError:  # Support for old API for backward compatibility
            momentum = self.schedule(epoch)
        if not isinstance(momentum, (float, np.float32, np.float64)):
            raise ValueError('The output of the "schedule" function '
                             'should be float.')
        # K.set_value(self.model.optimizer.lr, lr)
        self.model.optimizer.optimizer._momentum = momentum
        if self.verbose > 0:
            print('\nEpoch %05d: MomentumScheduler reducing momentum '
                  'rate to %s.' % (epoch + 1, momentum))

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['momentum'] = K.get_value(self.model.optimizer.optimizer._momentum)


class LearningRateScheduler(keras.callbacks.Callback):
    """Learning rate scheduler.
    # Arguments
    schedule: a function that takes an epoch index as input
    (integer, indexed from 0) and current learning rate
    and returns a new learning rate as output (float).
    verbose: int. 0: quiet, 1: update messages.
    """

    def __init__(self, schedule, verbose=0):
        super(LearningRateScheduler, self).__init__()
        self.schedule = schedule
        self.verbose = verbose

    def on_epoch_begin(self, epoch, logs=None):
        # if not hasattr(self.model.optimizer, 'lr'):   <=== Original  self.model.optimizer.optimizer._learning_rate
        if not hasattr(self.model.optimizer.optimizer, '_learning_rate'):
            raise ValueError('Optimizer must have a "_learning_rate" attribute.')
        try:  # new API
            # lr = float(K.get_value(self.model.optimizer.lr))
            lr = float(self.model.optimizer.optimizer._learning_rate)
            lr = self.schedule(epoch, lr)
        except TypeError:  # Support for old API for backward compatibility
            lr = self.schedule(epoch)
        if not isinstance(lr, (float, np.float32, np.float64)):
            raise ValueError('The output of the "schedule" function '
                             'should be float.')
        # K.set_value(self.model.optimizer.lr, lr)
        self.model.optimizer.optimizer._learning_rate = lr
        if self.verbose > 0:
            print('\nEpoch %05d: LearningRateScheduler reducing learning '
                  'rate to %s.' % (epoch + 1, lr))

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['lr'] = K.get_value(self.model.optimizer.optimizer._learning_rate)
